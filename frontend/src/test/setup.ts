// ABOUTME: Test setup file for Vitest with React Testing Library matchers
// ABOUTME: Imports jest-dom matchers for enhanced assertions and configures globals

import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});
