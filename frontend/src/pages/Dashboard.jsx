import React, { useEffect, useState } from 'react';
import { initializeSession, loadSession, saveSession } from '../utils/sessionManager';
import { supabase } from '../supabaseClient';
import ConstraintPanel from '../components/ConstraintPanel';
import WBSList from '../components/WBSList';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function Dashboard({ session: authSession }) {
  const [gameSession, setGameSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const loadGameSession = async () => {
      const userId = authSession.user.id;
      let session = loadSession(userId);

      if (!session) {
        // Initialize new session
        const wbsResponse = await fetch('/data/wbs.json');
        const wbsItems = await wbsResponse.json();

        const suppliersResponse = await fetch('/data/suppliers.json');
        const suppliers = await suppliersResponse.json();

        session = initializeSession(userId, wbsItems, suppliers);
      }

      setGameSession(session);
      setLoading(false);
    };

    loadGameSession();
  }, [authSession]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    navigate('/'); // Redirect to login after logout
  };

  if (loading) return <div>Laster økt...</div>;

  // Pass suppliers to WBSList
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Prosjektledelsessimulator</h1>
        <button onClick={handleLogout}>Logg Ut</button>
      </header>

      <ConstraintPanel
        budgetUsed={gameSession.metrics.total_budget_used}
        budgetLimit={700}
        projectedEndDate={gameSession.metrics.projected_end_date}
        deadline="2026-05-15"
      />

      <div className="quick-stats">
        Fremdrift: {Object.keys(gameSession.current_plan).length} / 15 WBS-oppgaver fullført |{' '}
        {gameSession.metrics.negotiation_count} forhandlinger
      </div>

      <WBSList
        wbsItems={gameSession.wbs_items}
        currentPlan={gameSession.current_plan}
        suppliers={gameSession.suppliers} // Pass suppliers here
        onSelectWBS={(wbsCode) => {
          // Navigate to supplier selection - this logic will be moved to WBSList/SupplierModal
          console.log('Selected WBS:', wbsCode);
        }}
      />
    </div>
  );
}

export default Dashboard;
