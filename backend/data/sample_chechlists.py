"""Sample checklists data for testing and demo purposes."""

SAMPLE_CHECKLISTS = [
    {
        'title': 'Project Setup Checklist',
        'description': 'Initial setup checklist for new projects',
        'items': [
            {'title': 'Create repository', 'order_index': 1},
            {'title': 'Set up development environment', 'order_index': 2},
            {'title': 'Configure CI/CD pipeline', 'order_index': 3},
        ]
    },
    {
        'title': 'Code Review Checklist',
        'description': 'Items to check during code review',
        'items': [
            {'title': 'Code follows style guidelines', 'order_index': 1},
            {'title': 'All tests passing', 'order_index': 2},
            {'title': 'Documentation updated', 'order_index': 3},
        ]
    },
    {
        'title': 'Deployment Checklist',
        'description': 'Pre-deployment verification steps',
        'items': [
            {'title': 'All tests pass in production environment', 'order_index': 1},
            {'title': 'Database migrations verified', 'order_index': 2},
            {'title': 'Backup created', 'order_index': 3},
        ]
    }
]
