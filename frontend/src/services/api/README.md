# API Services

This directory contains all the HTTP request functions for communicating with the backend API.

## Structure

```
api/
├── instance.ts     # Axios instance configuration
├── index.ts        # Main exports
├── thoughts/       # Thought-related API functions
├── publications/   # Publication-related API functions
├── categories/     # Category-related API functions
└── common/         # Common API functions (ex: health check)
```

## Usage

### Import API functions

```typescript
import {
  // Thought functions
  getThoughts,
  createThought,
  updateThought,
  deleteThought,
  getRelevantTopics,
  getRelatedThoughts,
  
  // Publication functions
  createPublicationPreview,
  createPublicationContent,
  
  // Category functions
  getCategories,
  
  // Common functions
  getHealth,
  
  // Types
  type Thought,
  type Publication,
  type Category,
  type CreateThoughtDTO,
  type UpdateThoughtDTO,
  // ... other types
} from '@/services/api';
```

### Examples

#### Thoughts

```typescript
// Get all thoughts
const thoughts = await getThoughts({});

// Search thoughts
const searchResults = await getThoughts({ search_term: "AI" });

// Create a new thought
await createThought({ text: "This is a new thought about AI and machine learning..." });

// Update a thought
const updatedThought = await updateThought({
  thought_id: "123",
  text: "Updated thought content..."
});

// Delete a thought
await deleteThought("123");

// Get related thoughts
const related = await getRelatedThoughts("123");

// Get topic suggestions
const topics = await getRelevantTopics("123");
```

#### Publications

```typescript
// Create publication preview
const preview = await createPublicationPreview({
  selected_thought_ids: ["<uuid>", "<uuid>"],
  publication_format: "blog_post",
  user_guideline: "Write in a professional tone"
});

// Create publication content
const publication = await createPublicationContent({
  publication_id: "<uuid>",
  publication_outlining: ["Introduction", "Main Content", "Conclusion"]
});
```

#### Categories

```typescript
// Get all categories
const categories = await getCategories();
```

#### Health Check

```typescript
// Check backend health
const health = await getHealth();
console.log(`Backend status: ${health.status}, version: ${health.version}`);
```

## Error Handling

All API functions use the configured Axios instance which includes:

- Request/response logging
- Automatic error handling for common HTTP status codes (401, 403, 404, 500)
- Network error detection
- Request timeout (100 seconds)

Errors are automatically logged and re-thrown, so you can handle them in your components:

```typescript
try {
  const thoughts = await getThoughts({});
} catch (error) {
  console.error('Failed to fetch thoughts:', error);
  // Handle error in your UI
}
```

## Configuration

The API base URL is configured via the `VITE_BACKEND_URL` environment variable, defaulting to `http://localhost:8000`.

You can override this in your `.env` file:

```env
VITE_BACKEND_URL='http://localhost:8000'
VITE_LOG_LEVEL='INFO'
``` 