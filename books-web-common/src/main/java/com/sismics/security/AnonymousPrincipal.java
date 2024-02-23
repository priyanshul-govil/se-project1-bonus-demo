java
package com.sismics.security;

import org.joda.time.DateTimeZone;

import java.util.Locale;

public class AnonymousPrincipal implements IPrincipal {
    public static final String ANONYMOUS = "anonymous";

    private Locale locale;
    private DateTimeZone dateTimeZone;

    public AnonymousPrincipal() {
        // Assign default values for fields to represent an anonymous user instead of null
        this.locale = Locale.getDefault();
        this.dateTimeZone = DateTimeZone.getDefault();
    }

    @Override
    public String getId() {
        // Return anonymous identifier instead of null
        return ANONYMOUS;
    }

    @Override
    public String getName() {
        return ANONYMOUS;
    }

    @Override
    public boolean isAnonymous() {
        return true;
    }

    @Override
    public Locale getLocale() {
        return locale;
    }

    public void setLocale(Locale locale) {
        this.locale = locale;
    }

    @Override
    public DateTimeZone getDateTimeZone() {
        return dateTimeZone;
    }

    public void setDateTimeZone(DateTimeZone dateTimeZone) {
        this.dateTimeZone = dateTimeZone;
    }

    @Override
    public String getEmail() {
        // As it's an anonymous principal, return a predefined value instead of null
        return "anonymous@noreply.com";
    }
}
