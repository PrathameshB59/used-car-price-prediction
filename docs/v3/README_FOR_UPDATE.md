# Documentation Update Pack

Date: 2026-08-19

This ZIP contains append-only documentation updates for the used-car
price prediction project.

The project instruction was to write new material without rewriting
existing documentation. Therefore these files are ADDENDUM files:
append each corresponding file to the existing documentation rather
than replacing the existing file.

Included:
- README.md.addendum
- CHANGELOG.md.addendum
- COMMAND.md.addendum
- HOW_TO_USE.md.addendum
- EXECUTION_PLAN.md.addendum
- WHAT_I_LEARNED.md.addendum

Important current project decisions recorded here:
- Backend: Django
- ML task: Regression
- Preprocessing: ColumnTransformer + OneHotEncoder
- Train/test split: 80/20, random_state=42
- Processed shapes: (12328, 165) and (3083, 165)
- Main ML model: RandomForestRegressor
- RandomForest training has not yet been completed at this update.
