import React from 'react';
import { useNavigate } from 'react-router-dom'; // Added this import
import SupplierModal from './SupplierModal'; // Added this import - will create next

function WBSList({ wbsItems, currentPlan, suppliers }) { // Added suppliers prop
  const [selectedWBS, setSelectedWBS] = React.useState(null); // Changed to React.useState
  const navigate = useNavigate();

  const handleSupplierSelect = (supplierId) => {
    navigate(`/chat/${selectedWBS.code}/${supplierId}`);
    setSelectedWBS(null); // Close modal after selection
  };

  return (
    <div className="wbs-list">
      <h2>Arbeidsnedbrytningsstruktur (WBS)</h2>
      {wbsItems.map((item) => {
        const isCompleted = currentPlan[item.code];
        return (
          <div key={item.code} className="wbs-item">
            <span className="status-icon">{isCompleted ? '🟢' : '⚪'}</span>
            <div className="wbs-content">
              <h4>{item.code} - {item.name}</h4>
              {isCompleted ? (
                <div className="wbs-details">
                  <p>{currentPlan[item.code].cost} MNOK, {currentPlan[item.code].duration} måneder</p>
                  <button onClick={() => setSelectedWBS(item)}>Reforhandle</button>
                </div>
              ) : (
                <div>
                  <p>Grunnlag: {item.baseline_cost} MNOK, {item.baseline_duration} måneder</p>
                  <button onClick={() => setSelectedWBS(item)}>Kontakt Leverandør</button>
                </div>
              )}
            </div>
          </div>
        );
      })}

      {selectedWBS && (
        <SupplierModal
          wbsItem={selectedWBS}
          suppliers={suppliers}
          onSelect={handleSupplierSelect}
          onClose={() => setSelectedWBS(null)}
        />
      )}
    </div>
  );
}

export default WBSList;
