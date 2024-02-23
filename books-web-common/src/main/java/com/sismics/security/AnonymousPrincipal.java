java
package com.sismics.security;

import org.joda.time.DateTimeZone;
import java.util.Locale;
import java.util.Optional;

/**
 * Anonymous principal.
 * 
 * @author jtremeaux
 */
public class AnonymousPrincipal implements IPrincipal {
    public static final String ANONYMOUS = "anonymous";
    
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
    public Optional<String> getId() {
        return Optional.empty();
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

    /**
     * Setter of locale.
     *
     * @param locale locale
     */
    public void setLocale(Locale locale) {
        this.locale = locale;
    }

    @Override
    public DateTimeZone getDateTimeZone() {
        return dateTimeZone;
    }

    @Override
    public Optional<String> getEmail() {
        return Optional.empty();
    }
    
    /**
     * Setter of dateTimeZone.
     *
     * @param dateTimeZone dateTimeZone
     */
    public void setDateTimeZone(DateTimeZone dateTimeZone) {
        this.dateTimeZone = dateTimeZone;
    }
}
