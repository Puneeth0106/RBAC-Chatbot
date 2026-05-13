import pandas as pd
from src.config import DATA_PATH

path = DATA_PATH / 'hr'
df = pd.read_csv(path / 'hr_data.csv')

with open(path / 'hr_data.md', 'w') as f:
    for i, row in df.iterrows():
        f.write(f"""## Employee: {row['full_name']}
- **Employee ID:** {row['employee_id']}
- **Role:** {row['role']}
- **Department:** {row['department']}
- **Email:** {row['email']}
- **Location:** {row['location']}
- **Date of Birth:** {row['date_of_birth']}
- **Date of Joining:** {row['date_of_joining']}
- **Manager ID:** {row['manager_id']}
- **Salary:** {row['salary']:,.2f}
- **Leave Balance:** {row['leave_balance']} | **Leaves Taken:** {row['leaves_taken']}
- **Attendance:** {row['attendance_pct']}%
- **Performance Rating:** {row['performance_rating']}
- **Last Review Date:** {row['last_review_date']}

---

""")

