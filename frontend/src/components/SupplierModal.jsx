import React from 'react';

function SupplierModal({ wbsItem, suppliers, onSelect, onClose }) {
  // Filter suppliers by relevant specialties
  const relevantSuppliers = suppliers.filter((s) =>
    s.specialties.some((spec) =>
      wbsItem.category.toLowerCase().includes(spec.toLowerCase()) ||
      wbsItem.name.toLowerCase().includes(spec.toLowerCase())
    )
  );

  // If no matches, show all suppliers
  const displaySuppliers = relevantSuppliers.length > 0 ? relevantSuppliers : suppliers;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>

        <h2>Velg Leverandør</h2>
        <p>WBS {wbsItem.code} - {wbsItem.name}</p>

        <div className="supplier-grid">
          {displaySuppliers.map((supplier) => (
            <div key={supplier.id} className="supplier-card" onClick={() => onSelect(supplier.id)}>
              <h3>{supplier.name}</h3>
              <p className="supplier-role">{supplier.role}</p>
              <p className="supplier-company">{supplier.company}</p>
              <p className="supplier-personality">{supplier.personality}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SupplierModal;
