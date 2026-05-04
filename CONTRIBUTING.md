# Contributing to PaperlessCheck

We're excited to have you contribute to PaperlessCheck! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Welcome all levels of experience
- Report issues professionally

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/PaperlessCheck.git
cd PaperlessCheck

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/PaperlessCheck.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 3. Set Up Development Environment

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Development Workflow

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

**JavaScript/React:**
- Use consistent naming (camelCase)
- Use functional components
- Keep components small and focused
- Add comments for complex logic

### Testing Before Commit

```bash
# Backend - Run with test data
cd backend
python app.py

# Frontend
cd frontend
npm run start
```

### Commit Messages

Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Build/dependency updates

Examples:
```
feat: add user authentication
fix: resolve checklist deletion bug
docs: update API documentation
```

### Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues (#123)
- Screenshots for UI changes
- Testing instructions

## Pull Request Process

1. **Title**: Clear and descriptive
2. **Description**: What does it do and why?
3. **Testing**: How can it be tested?
4. **Documentation**: Any docs to update?
5. **Screenshots**: If UI changes
6. **CI/CD**: Ensure all checks pass

## Types of Contributions

### Feature Requests

Open an issue with:
- Clear description of feature
- Use case and benefit
- Possible implementation approach
- Examples if applicable

### Bug Reports

Open an issue with:
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, browser, versions)
- Screenshots/logs

### Documentation

- Improve existing documentation
- Add examples
- Fix typos
- Add missing sections

### Code Review

- Review open pull requests
- Suggest improvements
- Test changes locally
- Share expertise

## Development Guidelines

### Backend Development

```python
# Good: Clear, descriptive function
def validate_checklist_data(data):
    """Validate checklist creation/update data.
    
    Args:
        data (dict): The checklist data to validate
        
    Returns:
        list: List of validation error messages (empty if valid)
    """
    errors = []
    
    if not data.get('title'):
        errors.append('Title is required')
    
    return errors

# Use proper error handling
try:
    result = some_operation()
except Exception as e:
    logger.error(f"Operation failed: {str(e)}")
    return jsonify({'error': 'Operation failed'}), 500
```

### Frontend Development

```javascript
// Good: Functional component with clear purpose
function ChecklistItem({ item, onToggle, onDelete }) {
  return (
    <li className={item.completed ? 'completed' : ''}>
      <label>
        <input
          type="checkbox"
          checked={item.completed}
          onChange={() => onToggle(item.id)}
        />
        <span>{item.title}</span>
      </label>
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  )
}

// Use proper error handling
const [error, setError] = useState('')

try {
  const response = await fetch(url)
  if (!response.ok) throw new Error('Request failed')
  const data = await response.json()
  setData(data)
} catch (err) {
  setError(err.message)
}
```

## Testing

### Manual Testing Checklist

- [ ] Feature works locally
- [ ] No console errors
- [ ] Responsive on mobile
- [ ] Database changes persist
- [ ] Error handling works
- [ ] No regression in existing features

### Testing Commands

```bash
# Backend health check
curl http://localhost:5000/api/health

# Frontend build
cd frontend && npm run build

# Docker build
docker-compose build --no-cache
```

## Documentation Requirements

### For New Features

1. **Code comments**: Explain complex logic
2. **Function docstrings**: What, why, parameters, returns
3. **README update**: Add feature description if user-facing
4. **API docs**: Update API endpoint documentation
5. **CHANGELOG**: If significant change

### For Bug Fixes

1. **Code comments**: Explain the fix
2. **Regression tests**: Add tests to prevent recurrence
3. **Issue reference**: Link to issue in commit/PR

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Tag release in git
5. Deploy to production

## Getting Help

- Check existing issues and PRs
- Ask in pull request comments
- Create a discussion issue
- Check documentation

## Acknowledgments

Thank you for contributing to make PaperlessCheck better! 🎉

Your contributions help the project grow and improve. Whether it's code, documentation, bug reports, or feature suggestions, every contribution matters.

---

**Happy Contributing! 🚀**
