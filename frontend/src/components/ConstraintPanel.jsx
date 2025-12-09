import React from 'react';

function ConstraintPanel({ budgetUsed, budgetLimit, projectedEndDate, deadline }) {
  const percentage = Math.round((budgetUsed / budgetLimit) * 100);
  const progressColor = percentage > 100 ? 'red' : percentage > 97 ? 'yellow' : 'green';

  const projDate = projectedEndDate ? new Date(projectedEndDate) : null;
  const deadlineDate = new Date(deadline);
  const onTime = projDate && projDate <= deadlineDate;

  return (
    <div className="constraint-panel">
      <div className="budget-section">
        <p>Budsjett: {budgetUsed} / {budgetLimit} MNOK ({percentage}%)</p>
        <div className="progress-bar">
          <div
            className={`progress-fill ${progressColor}`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
      </div>

      <div className="timeline-section">
        <p>Frist: {deadlineDate.toLocaleDateString('no-NO')}</p>
        {projDate && (
          <p>
            Forventet: {projDate.toLocaleDateString('no-NO')} {onTime ? '✓' : '✗'}
          </p>
        )}
      </div>
    </div>
  );
}

export default ConstraintPanel;
