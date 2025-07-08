# Poweradmin Features

Poweradmin provides comprehensive DNS management and administration capabilities. Here's an overview of the key features:

## Zone & Record Management

* Create and manage DNS zones (Master, Native, and Slave types)
* Support for supermasters for automatic provisioning of slave zones
* Full DNS record support:
    * A and AAAA records
    * CNAME records
    * HINFO records
    * MX records
    * NS records
    * PTR records (Reverse DNS)
    * SOA records
    * SRV records
    * TXT records
    * Other record types (supported but not validated)
* DNSSEC configuration and management
* IPv6 support

## Bulk Operations & Templates

* DNS record templates
* Default nameserver configuration
* Batch record creation
* PowerDNS API integration

## Security Features

* **Multi-Factor Authentication (MFA)**:
    * Support for authenticator apps (TOTP)
    * Email-based verification
    * Recovery codes for account recovery
    * Configurable recovery code generation
* **Advanced Account Lockout**:
    * Login attempt tracking with database support
    * Configurable lockout attempts and duration
    * IP address-based tracking and lockouts
    * Whitelist and blacklist support (supports IPs, CIDRs, wildcards)
* **Password Reset System**:
    * Secure password reset via email
    * Configurable token lifetime and rate limiting
    * Protection against brute force attacks
* **Google reCAPTCHA Integration**:
    * Support for reCAPTCHA v2 and v3
    * Configurable score thresholds for v3
    * Login form protection
* **Enhanced Password Policies**:
    * Configurable minimum length requirements
    * Character type requirements (uppercase, lowercase, numbers, special)
    * Custom special character sets
* **Traditional Security Features**:
    * LDAP/Active Directory integration with custom filter
    * CSRF prevention
    * Session security
    * SSL/TLS support

## System Integration

* Database support:
    * MySQL/MariaDB integration
    * PostgreSQL support
    * SQLite support
    * Optimized for large databases (tested with 15,000+ zones and 150,000+ records)
    * Configurable connections
* Email notifications:
    * Multiple transport methods
    * Template customization
* Configuration:
    * Default settings
    * Environment-specific overrides

## User Interface

* **Modern Responsive Design**:
    * Bootstrap-based responsive interface
    * Mobile-friendly design
    * Customizable elements
* **Theming System**:
    * Light and dark mode support
    * Customizable theme base paths
    * Theme selection per user preference
* **Multi-language Support**:
    * 15 supported languages
    * Gettext-based translations
    * Right-to-left language support
* **User Preferences**:
    * Personalized user settings storage
    * Individual user customization options
    * Per-user theme preferences
* **Enhanced Interface Options**:
    * Display full names instead of usernames in zone lists
    * Improved reverse zone sorting (natural or hierarchical)
    * PowerDNS server status integration
    * Database consistency checks page
    * Email template previews
* **Error Management**:
    * Development mode
    * Production mode

## Logging & Monitoring

* Logging features:
    * Native system logging
    * Syslog integration
    * Change tracking
    * Configurable levels
* Monitoring:
    * System statistics
    * Conflict detection

## API Management (v4.0.0+)

* **API Key System**:
    * Generate and manage API keys for external integrations
    * Key-based authentication for API endpoints
    * Request logging and monitoring
    * API documentation endpoints
* **RESTful API Endpoints**:
    * Zone management (create, read, update, delete)
    * DNS record management
    * User management
    * Permission template management
    * Internal API for UI components

## Lookup and Integration Features (v4.0.0+)

* **WHOIS Lookup**:
    * Built-in WHOIS query functionality
    * Configurable WHOIS servers
    * Socket timeout controls
    * Admin-only access controls
* **RDAP Lookup**:
    * Registration Data Access Protocol support
    * HTTP-based domain information queries
    * Configurable RDAP servers
    * Request timeout controls

## Zone Management Enhancements (v4.0.0+)

* **Zone Template Synchronization**:
    * Automatic synchronization of zone templates
    * Template change tracking
    * Batch operations support
* **User Agreements System**:
    * Version-controlled user agreements
    * Automatic re-acceptance on version changes
    * Compliance tracking
* **DNS Record Type Customization**:
    * Customize which record types are available
    * Separate configuration for forward and reverse zones
    * Simplified interface for specific DNS needs

## Additional Documentation

* [Security Configuration](../configuration/security-policies.md)
* [Database Setup](../configuration/database.md)
* [DNS Configuration](../configuration/dns-settings.md)
* [Logging Options](../configuration/logging.md)
* [API Configuration](../configuration/api.md)
* [Multi-Factor Authentication](../configuration/security-policies.md#multi-factor-authentication)
* [WHOIS Configuration](../configuration/whois.md)
* [RDAP Configuration](../configuration/rdap.md)