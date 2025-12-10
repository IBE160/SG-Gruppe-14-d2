// Session schema based on PRD Section 8
export const initializeSession = (userId, wbsItems, suppliers) => {
  const sessionId = `session_${userId}_${Date.now()}`;
  const session = {
    game_id: sessionId,
    user_id: userId,
    created_at: new Date().toISOString(),
    status: 'in_progress',
    wbs_items: wbsItems,
    suppliers: suppliers,
    current_plan: {},
    plan_history: [],
    chat_logs: {},
    metrics: {
      total_budget_used: 0,
      projected_end_date: null,
      negotiation_count: 0,
      renegotiation_count: 0,
    },
  };

  localStorage.setItem(`nye_haedda_session_${userId}`, JSON.stringify(session));
  return session;
};

export const loadSession = (userId) => {
  const saved = localStorage.getItem(`nye_haedda_session_${userId}`);
  return saved ? JSON.parse(saved) : null;
};

export const saveSession = (session) => {
  localStorage.setItem(`nye_haedda_session_${session.user_id}`, JSON.stringify(session));
};

export const commitQuote = (session, wbsCode, supplierId, cost, duration) => {
  // Calculate start_date based on dependencies
  const wbsItem = session.wbs_items.find((item) => item.code === wbsCode);
  let startDate = new Date('2025-01-15'); // Default project start

  if (wbsItem.dependencies.length > 0) {
    // Find latest end_date from dependencies
    const depEndDates = wbsItem.dependencies.map((depCode) => {
      const depPlan = session.current_plan[depCode];
      return depPlan ? new Date(depPlan.end_date) : startDate;
    });
    startDate = new Date(Math.max(...depEndDates));
    startDate.setDate(startDate.getDate() + 1); // Start next day
  }

  const endDate = new Date(startDate);
  endDate.setMonth(endDate.getMonth() + duration);

  session.current_plan[wbsCode] = {
    supplier_id: supplierId,
    cost,
    duration,
    start_date: startDate.toISOString().split('T')[0],
    end_date: endDate.toISOString().split('T')[0],
  };

  session.plan_history.push({
    timestamp: new Date().toISOString(),
    action: 'commit',
    wbs_code: wbsCode,
    supplier_id: supplierId,
    cost,
    duration,
  });

  session.metrics.total_budget_used = Object.values(session.current_plan).reduce(
    (sum, item) => sum + item.cost,
    0
  );

  // Calculate projected end date (max end_date from all committed items)
  const allEndDates = Object.values(session.current_plan).map((item) => new Date(item.end_date));
  session.metrics.projected_end_date = new Date(Math.max(...allEndDates))
    .toISOString()
    .split('T')[0];

  saveSession(session);
  return session;
};

export const removeQuote = (session, wbsCode) => {
  const removedItem = session.current_plan[wbsCode];
  delete session.current_plan[wbsCode];

  session.plan_history.push({
    timestamp: new Date().toISOString(),
    action: 'remove',
    wbs_code: wbsCode,
    reason: 'renegotiation',
  });

  session.metrics.renegotiation_count += 1;

  saveSession(session);
  return session;
};

export const validatePlan = (session) => {
  const totalCost = session.metrics.total_budget_used;
  const budgetLimit = 700; // MNOK
  const deadline = new Date('2026-05-15');
  const projectedDate = new Date(session.metrics.projected_end_date);

  const errors = [];

  if (totalCost > budgetLimit) {
    errors.push({
      type: 'budget',
      message: `Budsjett overskredet med ${totalCost - budgetLimit} MNOK (Total: ${totalCost}, Grense: ${budgetLimit})`,
      overage: totalCost - budgetLimit,
    });
  }

  if (projectedDate > deadline) {
    const daysLate = Math.floor((projectedDate - deadline) / (1000 * 60 * 60 * 24));
    errors.push({
      type: 'timeline',
      message: `Prosjektet forsinket til ${projectedDate.toLocaleDateString('no-NO')} (Frist: ${deadline.toLocaleDateString('no-NO')})`,
      daysLate,
    });
  }

  const completedCount = Object.keys(session.current_plan).length;
  if (completedCount < 15) {
    errors.push({
      type: 'incomplete',
      message: `Kun ${completedCount} / 15 oppgaver fullført`,
    });
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};
