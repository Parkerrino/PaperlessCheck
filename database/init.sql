-- Create checklists table
CREATE TABLE IF NOT EXISTS checklists (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create checklist_items table
CREATE TABLE IF NOT EXISTS checklist_items (
    id SERIAL PRIMARY KEY,
    checklist_id INTEGER NOT NULL REFERENCES checklists(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for better performance
CREATE INDEX idx_checklist_items_checklist_id ON checklist_items(checklist_id);

-- Insert sample data
INSERT INTO checklists (title, description) VALUES
    ('Project Setup Checklist', 'Initial setup checklist for new projects'),
    ('Code Review Checklist', 'Items to check during code review'),
    ('Deployment Checklist', 'Pre-deployment verification steps');

INSERT INTO checklist_items (checklist_id, title, order_index) VALUES
    (1, 'Create repository', 1),
    (1, 'Set up development environment', 2),
    (1, 'Configure CI/CD pipeline', 3),
    (2, 'Code follows style guidelines', 1),
    (2, 'All tests passing', 2),
    (2, 'Documentation updated', 3),
    (3, 'All tests pass in production environment', 1),
    (3, 'Database migrations verified', 2),
    (3, 'Backup created', 3);
