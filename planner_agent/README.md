Why it matters
Right now your coordinator likely:

routes

splits

aggregates

What it doesn’t fully do yet:

generate an explicit execution plan

reason about dependencies

decide ordering vs parallelism

What to add

A Planner Agent that:

converts prompt → structured plan (JSON)

identifies:

steps

required agents/tools

dependencies

stop conditions

Result

Better multi-step reasoning

Easier debugging

Safer autonomy

This is the single most impactful upgrade.