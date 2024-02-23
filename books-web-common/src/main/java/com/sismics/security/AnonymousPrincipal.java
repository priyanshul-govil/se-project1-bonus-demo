java
package com.sismics.security;

import org.joda.time.DateTimeZone;

import java.util.Locale;

/**
 * Anonymous principal.
 *
 * @author jtremeaux
 */
public class AnonymousPrincipal implements IPrincipal {
    public static final String ANONYMOUS = "anonymous";
    public static final String NO_EMAIL = "no-email@anonymous.com";

    /**
     * User locale.
     */
    private final Locale locale;

    /**
     * User timezone.
     */
    private final DateTimeZone dateTimeZone;

    /**
     * Constructor of AnonymousPrincipal.
     *
     * @param locale local of the user
     * @param dateTimeZone timezone of the user
     */
    public AnonymousPrincipal(Locale locale, DateTimeZone dateTimeZone) {
        this.locale = locale;
        this.dateTimeZone = dateTimeZone;
    }

    @Override
    public String getId() {
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

    @Override
    public DateTimeZone getDateTimeZone() {
        return dateTimeZone;
    }

    @Override
    public String getEmail() {
        return NO_EMAIL;
    }
}
