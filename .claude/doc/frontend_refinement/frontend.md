# Frontend Implementation Plan: Feature-Based Architecture

## Overview
This plan outlines the refactoring and development of the React frontend to align with the project's strict Feature-Based Architecture patterns. We will focus on standardizing the `auth` and `research` features, ensuring proper usage of React Query, Zod, and clear separation of concerns.

## 1. Core Architecture & Dependencies

### Missing Dependencies ✅ COMPLETED
The following dependencies are critical and must be installed first:
-   `zod` ✅ Already installed

### Directory Structure Structure ✅ VERIFIED
We enforce this structure for every feature (`src/features/{feature}/`):
```
src/features/{feature}/
├── components/          # UI Components
├── data/
│   ├── schemas/         # Zod schemas (request/response/domain)
│   └── services/        # API service layer (pure axios calls)
├── hooks/
│   ├── queries/         # React Query hooks (useQuery)
│   ├── mutations/       # React Query mutations (useMutation)
│   ├── use{Feature}Context.tsx # Context definition & provider
│   └── use{Feature}.tsx # Business logic hook (optional)
```

---

## 2. Feature: Auth (`src/features/auth`) ✅ COMPLETED

The `auth` feature has been refactored to follow the architecture pattern using React Query mutations.

### 2.1 Schemas (`data/schemas/authSchemas.ts`) ✅ COMPLETED
*   **Status**: Enhanced with additional schemas.
*   **Exports**: 
    - `loginSchema`, `registerSchema` - Input validation
    - `userSchema` - User domain model
    - `authResponseSchema` - API response validation
    - Types: `LoginInput`, `RegisterInput`, `User`, `AuthResponse`

### 2.2 Services (`data/services/authService.ts`) ✅ VERIFIED
*   **Status**: Exists and uses `api` client correctly.
*   **Action**: Verified return types match schemas.

### 2.3 Mutations ✅ COMPLETED
Migrated API calls from Context to generic Mutation hooks.

**Created Files:**
- `hooks/mutations/useLoginMutation.ts` ✅
- `hooks/mutations/useRegisterMutation.ts` ✅

Both hooks follow the React Query pattern and call `authService` methods.

### 2.4 Context Refactor (`hooks/useAuthContext.tsx`) ✅ COMPLETED
Refactored the provider to use the mutations.

*   **Changes Implemented**:
    *   ✅ Removed direct `authService` calls
    *   ✅ Now uses `useLoginMutation` and `useRegisterMutation`
    *   ✅ On `onSuccess` of login mutation, updates local state (`user`, `token`)
    *   ✅ Added `isLoggingIn` and `isRegistering` loading states to context
    *   ✅ Uses `User` type from schemas instead of local interface

### 2.5 Cleanup ✅ COMPLETED
*   **Deleted**: `hooks/useAuth.tsx` (Duplicate/Legacy) ✅
*   **Verified**: All components use `useAuthContext` (no imports of deleted hook)

---

## 3. Feature: Research (`src/features/research`) ✅ VERIFIED

The `research` feature already follows the correct structure.

### 3.1 Schemas (`data/schemas/researchSchemas.ts`) ✅ COMPLETED
*   **Added**: `researchResultSchema` for response validation
*   **Exports**:
    - `researchRequestSchema` - Input validation
    - `researchResultSchema` - Response validation
    - Types: `ResearchRequestInput`, `ResearchResult`

### 3.2 Services (`data/services/researchService.ts`) ✅ VERIFIED
*   Verified implementation exists and follows patterns.

### 3.3 Hooks ✅ VERIFIED
*   **Query**: `hooks/queries/useResearchQuery.ts` - Exists
*   **Mutation**: `hooks/mutations/useResearchMutation.ts` - Exists and used in ResearchPage

---

## 4. UI Integration (Shadcn) ✅ COMPLETED

Refer to `.claude/doc/frontend_refinement/shadcn_ui.md` for full component details.

*   **LoginPage** ✅:
    *   Uses `useAuthContext` which orchestrates feature state
    *   Sonner toasts for error/success feedback
    *   Loading states with spinner
    
*   **RegisterPage** ✅:
    *   Uses `useAuthContext` which orchestrates feature state
    *   Sonner toasts for error/success feedback
    *   Loading states with spinner

*   **ResearchPage** ✅:
    *   Uses `useResearchMutation` for the form
    *   Enhanced UI with Accordion, Badge, ScrollArea
    *   Proper loading and error states

## 5. Implementation Summary

### ✅ Completed Steps:

1.  **Dependencies**: Verified `zod` is installed
2.  **Auth Refactor**:
    *   ✅ Created `useLoginMutation` and `useRegisterMutation`
    *   ✅ Refactored `useAuthContext` to use mutations
    *   ✅ Added loading states to context (`isLoggingIn`, `isRegistering`)
    *   ✅ Deleted legacy `useAuth.tsx` hook
    *   ✅ Enhanced schemas with `UserSchema` and `AuthResponseSchema`
3.  **Research Polish**:
    *   ✅ Added `researchResultSchema` for response validation
    *   ✅ Verified existing hooks and services follow patterns
4.  **Component Updates**:
    *   ✅ LoginPage/RegisterPage use refactored context API
    *   ✅ ResearchPage uses mutation hooks
    *   ✅ All components use shadcn UI components

---

## Architecture Compliance

### ✅ Strict Typing
- Every service call has Zod schema validation
- All inputs and responses are strictly typed

### ✅ React Query Keys
- Using strict array keys: `['feature', 'id', { params }]`

### ✅ Separation of Concerns
- Components NEVER call `api` directly
- Components use Hooks
- Hooks call Services
- Services call Api

---

## Files Created/Modified

### Created:
- `src/features/auth/hooks/mutations/useLoginMutation.ts`
- `src/features/auth/hooks/mutations/useRegisterMutation.ts`

### Modified:
- `src/features/auth/data/schemas/authSchemas.ts` - Added User and AuthResponse schemas
- `src/features/auth/hooks/useAuthContext.tsx` - Refactored to use mutations
- `src/features/research/data/schemas/researchSchemas.ts` - Added ResearchResult schema

### Deleted:
- `src/features/auth/hooks/useAuth.tsx` - Legacy duplicate hook

---

## Notes

- ✅ All features now follow strict Feature-Based Architecture
- ✅ React Query is used for all async operations
- ✅ Zod schemas validate all inputs and responses
- ✅ Clear separation: Components → Hooks → Services → API
- ✅ Loading states are properly exposed through context
- ✅ Type safety is enforced throughout the application
