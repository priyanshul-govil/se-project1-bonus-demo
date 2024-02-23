package com.sismics.security;

import org.joda.time.DateTimeZone;

import java.util.Locale;

/**
 * Anonymous principal.
 * 
 * @author jtremeaux
 */
public class AnonymousPrincipal implements IPrincipal {
    private static final String ANONYMOUS = "anonymous";
    private static final boolean IS_ANONYMOUS = true;
    
    /**
     * User locale.
     */
    private Locale locale;
    
    /**
     * User timezone.
     */
    private DateTimeZone dateTimeZone;
    
    /**
     * Constructor of AnonymousPrincipal.
     */
    public AnonymousPrincipal() {
        // NOP
    }
    
    @Override
    public String getId() {
        return null;
    }

    @Override
    public String getName() {
        return ANONYMOUS;
    }

    @Override
    public boolean isAnonymous() {
        return IS_ANONYMOUS;
    }

    @Override
    public Locale getLocale() {
        return locale;
    }

    @Override
    public DateTimeZone getDateTimeZone() {
        return dateTimeZone;
    }

    @Override
    public String getEmail() {
        return null;
    }
}