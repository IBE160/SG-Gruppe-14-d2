"""
Critical Path Method (CPM) calculation service.

Implements forward pass (ES/EF) and backward pass (LS/LF) algorithms
to calculate the critical path for WBS items.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple


class CriticalPathCalculator:
    """
    Calculates critical path using CPM (Critical Path Method) algorithm.

    Forward pass: Calculate Earliest Start (ES) and Earliest Finish (EF)
    Backward pass: Calculate Latest Start (LS) and Latest Finish (LF)
    Critical path: Tasks where slack = 0 (LS - ES = 0)
    """

    def __init__(self, wbs_items: List[Dict], start_date: str = "2025-01-15"):
        """
        Initialize calculator with WBS items.

        Args:
            wbs_items: List of WBS items with id, duration, dependencies
            start_date: Project start date in YYYY-MM-DD format
        """
        self.wbs_items = {item['id']: item for item in wbs_items}
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")

        # Results
        self.earliest_start: Dict[str, datetime] = {}
        self.earliest_finish: Dict[str, datetime] = {}
        self.latest_start: Dict[str, datetime] = {}
        self.latest_finish: Dict[str, datetime] = {}
        self.slack: Dict[str, int] = {}
        self.critical_path: List[str] = []

    def get_duration(self, wbs_id: str, commitments: Dict[str, Dict]) -> int:
        """
        Get duration for a WBS item from commitment or baseline.

        Args:
            wbs_id: WBS item ID
            commitments: Dict mapping wbs_id to commitment data

        Returns:
            Duration in days
        """
        item = self.wbs_items[wbs_id]

        # Check if there's a commitment with duration
        if wbs_id in commitments and commitments[wbs_id].get('duration'):
            return commitments[wbs_id]['duration']

        # Otherwise use baseline or locked duration
        if item.get('is_negotiable'):
            return item.get('baseline_duration', 0)
        else:
            return item.get('locked_duration', 0)

    def topological_sort(self) -> List[str]:
        """
        Perform topological sort on WBS items based on dependencies.

        Returns:
            List of WBS IDs in topologically sorted order
        """
        # Build in-degree map
        in_degree = {wbs_id: 0 for wbs_id in self.wbs_items}

        for wbs_id, item in self.wbs_items.items():
            dependencies = item.get('dependencies', [])
            in_degree[wbs_id] = len(dependencies)

        # Queue with nodes having no dependencies
        queue = [wbs_id for wbs_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            # Find all tasks that depend on current task
            for wbs_id, item in self.wbs_items.items():
                dependencies = item.get('dependencies', [])
                if current in dependencies:
                    in_degree[wbs_id] -= 1
                    if in_degree[wbs_id] == 0:
                        queue.append(wbs_id)

        # Check for cycles
        if len(result) != len(self.wbs_items):
            raise ValueError("Circular dependency detected in WBS items")

        return result

    def forward_pass(self, commitments: Dict[str, Dict]):
        """
        Forward pass: Calculate Earliest Start (ES) and Earliest Finish (EF).

        ES = max(EF of all predecessors)
        EF = ES + duration

        Args:
            commitments: Dict mapping wbs_id to commitment data
        """
        sorted_tasks = self.topological_sort()

        for wbs_id in sorted_tasks:
            item = self.wbs_items[wbs_id]
            dependencies = item.get('dependencies', [])
            duration = self.get_duration(wbs_id, commitments)

            if not dependencies:
                # No dependencies, start at project start date
                self.earliest_start[wbs_id] = self.start_date
            else:
                # Start after all dependencies finish
                max_ef = max(self.earliest_finish[dep] for dep in dependencies)
                self.earliest_start[wbs_id] = max_ef

            # Calculate earliest finish
            self.earliest_finish[wbs_id] = self.earliest_start[wbs_id] + timedelta(days=duration)

    def backward_pass(self, commitments: Dict[str, Dict], deadline: datetime):
        """
        Backward pass: Calculate Latest Start (LS) and Latest Finish (LF).

        LF = min(LS of all successors), or deadline for final tasks
        LS = LF - duration

        Args:
            commitments: Dict mapping wbs_id to commitment data
            deadline: Project deadline
        """
        sorted_tasks = list(reversed(self.topological_sort()))

        # Build successor map
        successors: Dict[str, List[str]] = {wbs_id: [] for wbs_id in self.wbs_items}
        for wbs_id, item in self.wbs_items.items():
            dependencies = item.get('dependencies', [])
            for dep in dependencies:
                successors[dep].append(wbs_id)

        for wbs_id in sorted_tasks:
            duration = self.get_duration(wbs_id, commitments)

            if not successors[wbs_id]:
                # No successors, finish at deadline
                self.latest_finish[wbs_id] = deadline
            else:
                # Finish before all successors start
                min_ls = min(self.latest_start[succ] for succ in successors[wbs_id])
                self.latest_finish[wbs_id] = min_ls

            # Calculate latest start
            self.latest_start[wbs_id] = self.latest_finish[wbs_id] - timedelta(days=duration)

    def calculate_slack(self):
        """
        Calculate slack time for each task.

        Slack = LS - ES = LF - EF
        Critical path tasks have slack = 0
        """
        for wbs_id in self.wbs_items:
            slack_days = (self.latest_start[wbs_id] - self.earliest_start[wbs_id]).days
            self.slack[wbs_id] = slack_days

            if slack_days == 0:
                self.critical_path.append(wbs_id)

    def calculate(self, commitments: Dict[str, Dict], deadline: str = "2026-05-15") -> Dict:
        """
        Run full CPM calculation.

        Args:
            commitments: Dict mapping wbs_id to commitment data
            deadline: Project deadline in YYYY-MM-DD format

        Returns:
            Dict with ES, EF, LS, LF, critical path, and validation results
        """
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")

        # Run forward and backward passes
        self.forward_pass(commitments)
        self.backward_pass(commitments, deadline_dt)
        self.calculate_slack()

        # Find project completion date (max EF)
        if self.earliest_finish:
            projected_completion = max(self.earliest_finish.values())
        else:
            projected_completion = self.start_date

        meets_deadline = projected_completion <= deadline_dt

        # Format results
        return {
            "valid": meets_deadline,
            "earliest_start": {
                wbs_id: date.strftime("%Y-%m-%d")
                for wbs_id, date in self.earliest_start.items()
            },
            "earliest_finish": {
                wbs_id: date.strftime("%Y-%m-%d")
                for wbs_id, date in self.earliest_finish.items()
            },
            "latest_start": {
                wbs_id: date.strftime("%Y-%m-%d")
                for wbs_id, date in self.latest_start.items()
            },
            "latest_finish": {
                wbs_id: date.strftime("%Y-%m-%d")
                for wbs_id, date in self.latest_finish.items()
            },
            "slack": self.slack,
            "critical_path": self.critical_path,
            "projected_completion_date": projected_completion.strftime("%Y-%m-%d"),
            "deadline": deadline,
            "meets_deadline": meets_deadline,
            "total_duration_days": (projected_completion - self.start_date).days
        }


def calculate_critical_path(wbs_items: List[Dict], commitments: List[Dict],
                           start_date: str = "2025-01-15",
                           deadline: str = "2026-05-15") -> Dict:
    """
    Calculate critical path for WBS items with commitments.

    Args:
        wbs_items: List of WBS items from wbs.json
        commitments: List of commitment records from database
        start_date: Project start date
        deadline: Project deadline

    Returns:
        Dict with timeline data, critical path, and validation results
    """
    # Convert commitments list to dict for easier lookup
    commitment_map = {
        c['wbs_item_id']: c
        for c in commitments
    }

    # Initialize calculator and run CPM
    calculator = CriticalPathCalculator(wbs_items, start_date)
    result = calculator.calculate(commitment_map, deadline)

    return result
