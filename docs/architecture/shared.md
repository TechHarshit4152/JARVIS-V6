# Shared Architecture

## Purpose

The Shared subsystem contains reusable components that are common across multiple subsystems.

It exists to eliminate duplication while maintaining clear boundaries between subsystems.

The Shared subsystem does not contain business logic.

Its responsibility is reusability.

---

## Responsibilities

The Shared subsystem is responsible for:

- Common data models
- Shared interfaces
- Common enums
- Constants
- Utility functions
- Validation helpers
- Common exceptions
- Type definitions

The Shared subsystem provides common building blocks used throughout JARVIS.

---

## Owns

The Shared subsystem owns:

- Data Transfer Objects (DTOs)
- Base Interfaces
- Enums
- Constants
- Utility Functions
- Validators
- Exceptions
- Common Types

---

## Allowed

The Shared subsystem is allowed to:

- Define reusable models
- Define interfaces
- Define constants
- Define helper utilities
- Define common validation logic
- Define shared exceptions

---

## Forbidden

The Shared subsystem must never:

- Perform reasoning
- Execute tools
- Store memories
- Handle HTTP requests
- Implement module logic
- Access databases
- Modify UI
- Manage application lifecycle

Shared provides reusable code.

It never owns system behavior.

---

## Dependencies

The Shared subsystem may depend on:

- Standard Library

The Shared subsystem should never directly depend on:

- Core
- AI
- Memory
- Tools
- Modules
- Database
- Frontend
- Backend

Shared should remain as dependency-free as possible.

---

## Public API

The Shared subsystem exposes:

- Common Models
- Common Interfaces
- Constants
- Enums
- Validators
- Utility Functions

These components may be used throughout JARVIS.

---

## Future Expansion

Future versions may include:

- Serialization Helpers
- Common Configuration Types
- Event Definitions
- Error Codes
- Shared Protocols
- Versioned Contracts

These additions must preserve Shared's role as a reusable foundation.

---

## Design Principles

The Shared subsystem follows these principles:

- Reuse over duplication
- Simplicity
- Dependency independence
- Predictability
- Consistency

---

## Golden Rule

Shared contains reusable building blocks—it never contains business logic.