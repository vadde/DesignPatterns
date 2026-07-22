# Design Patterns Repository — Planning Prompt

> This file archives the original prompt and conversation that led to the creation of this repository.

## Original Request (2025-07-22)

The user requested a comprehensive Design Patterns repository mirroring the structure and quality of the existing DSA repository. Key requirements:

1. **Same structure as DSA**: Git repository, numbered chapters, `theory.md` + code files per chapter
2. **All experience levels**: Tutor, instructor, architect, professor, engineer perspectives
3. **Prioritize visuals**: Diagrams, charts, flows — pictorial over prose
4. **Python 3.14**: Strict baseline with Django, FastAPI, SQLAlchemy framework examples
5. **Notebook-style**: Centralized README as clickable appendix
6. **ReAct + Reflexion**: Every bit analyzed, correlated, and concluded with full semantics
7. **Same Git remotes**: Mirror the DSA repo setup

## Approved Plan

- **26 chapters** across 4 parts (Foundations + Creational + Structural + Behavioral + Advanced)
- **Flat directory naming**: `NN - Pattern Name (Category)/`
- **Theory template**: Adapted from DSA with UML class/sequence diagrams, framework sightings, SOLID connections
- **Code template**: `example_NN_slug.py` format with real-world scenarios
- **Phased execution**: Foundations → Creational → Structural → Behavioral → Advanced

## Reference: DSA Repo Structure

The DSA repository uses:
- `NN - Pattern Name/` directories
- `theory.md` per pattern
- `problem_NN_slug.py` per problem
- `_internal/instructions.md` as agent system prompt
- Centralized `README.md` as appendix
