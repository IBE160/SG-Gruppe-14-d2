-- PART 2: INDEXES AND RLS POLICIES
-- Run this AFTER Part 1 succeeds

-- CREATE INDEXES
CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_game_sessions_status ON public.game_sessions(status);
CREATE INDEX IF NOT EXISTS idx_wbs_commitments_session_id ON public.wbs_commitments(session_id);
CREATE INDEX IF NOT EXISTS idx_negotiation_history_session_id ON public.negotiation_history(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_timeouts_session_agent ON public.agent_timeouts(session_id, agent_id);

-- ENABLE ROW LEVEL SECURITY
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wbs_commitments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.negotiation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_timeouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;

-- RLS POLICIES
CREATE POLICY "Users can view their own sessions"
    ON public.game_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own sessions"
    ON public.game_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions"
    ON public.game_sessions FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view commitments for their sessions"
    ON public.wbs_commitments FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = wbs_commitments.session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can insert commitments for their sessions"
    ON public.wbs_commitments FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can view their negotiation history"
    ON public.negotiation_history FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = negotiation_history.session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can insert their negotiation history"
    ON public.negotiation_history FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can view their own analytics"
    ON public.user_analytics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own analytics"
    ON public.user_analytics FOR INSERT
    WITH CHECK (auth.uid() = user_id);
