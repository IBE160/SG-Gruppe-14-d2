-- PART 3: TRIGGERS AND VIEWS
-- Run this AFTER Part 2 succeeds

-- CREATE TRIGGER FUNCTION
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- CREATE TRIGGERS
DROP TRIGGER IF EXISTS update_game_sessions_updated_at ON public.game_sessions;
CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON public.game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_analytics_updated_at ON public.user_analytics;
CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- CREATE VIEWS
CREATE OR REPLACE VIEW active_sessions_summary AS
SELECT
    gs.id,
    gs.user_id,
    gs.status,
    gs.current_budget_used,
    gs.budget_tier1_percentage,
    gs.budget_remaining,
    COUNT(DISTINCT wc.id) as commitments_count,
    COUNT(DISTINCT nh.id) as negotiation_messages_count,
    gs.created_at,
    gs.updated_at
FROM public.game_sessions gs
LEFT JOIN public.wbs_commitments wc ON wc.session_id = gs.id
LEFT JOIN public.negotiation_history nh ON nh.session_id = gs.id
WHERE gs.status = 'in_progress'
GROUP BY gs.id;

CREATE OR REPLACE VIEW leaderboard AS
SELECT
    ua.user_id,
    ua.total_sessions,
    ua.completed_sessions,
    ua.total_savings,
    ua.average_savings_percentage,
    ua.best_savings_percentage,
    RANK() OVER (ORDER BY ua.average_savings_percentage DESC) as rank
FROM public.user_analytics ua
WHERE ua.completed_sessions > 0
ORDER BY ua.average_savings_percentage DESC;
