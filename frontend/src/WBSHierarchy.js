import React from 'react';

// Helper function to build a hierarchical structure from a flat list
const buildHierarchy = (items) => {
  const root = { children: [] };
  const map = { "0": root }; // Use "0" as a virtual root for top-level items

  items.forEach(item => {
    map[item.id] = { ...item, children: [] };
  });

  items.forEach(item => {
    const parentId = item.id.substring(0, item.id.lastIndexOf('.'));
    const parent = map[parentId] || root; // If no parentId, it's a top-level item
    if (parent) {
      parent.children.push(map[item.id]);
    }
  });
  return root.children;
};

// Recursive component to render WBS items
const WBSItem = ({ item }) => {
  return (
    <li>
      <strong>{item.id}</strong>: {item.name} ({item.status})
      {item.children.length > 0 && (
        <ul>
          {item.children.map(child => (
            <WBSItem key={child.id} item={child} />
          ))}
        </ul>
      )}
    </li>
  );
};

const WBSHierarchy = ({ wbsData }) => {
  const hierarchicalData = buildHierarchy(wbsData);

  return (
    <ul>
      {hierarchicalData.map(item => (
        <WBSItem key={item.id} item={item} />
      ))}
    </ul>
  );
};

export default WBSHierarchy;
