java
package com.sismics.security;

import org.joda.time.DateTimeZone;

import java.util.Locale;

/**
 * Abstract principal.
 * 
 * @author jtremeaux
 */

public abstract class AbstractPrincipal implements IPrincipal {

    protected Locale locale;
    protected DateTimeZone dateTimeZone;

    protected AbstractPrincipal(Locale locale, DateTimeZone dateTimeZone) {
        this.locale = locale;
        this.dateTimeZone = dateTimeZone;
    }

    @Override
    public boolean isAnonymous() {
        return false;
    }

    @Override
    public Locale getLocale() {
        return locale;
    }

    @Override
    public DateTimeZone getDateTimeZone() {
        return dateTimeZone;
    }
}

/**
 * Anonymous principal.
 * 
 * @author jtremeaux
 */
public class AnonymousPrincipal extends AbstractPrincipal {

    public static final String ANONYMOUS = "anonymous";

    public AnonymousPrincipal(Locale locale, DateTimeZone dateTimeZone) {
        super(locale, dateTimeZone);
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
        return true;
    }

    @Override
    public String getEmail() {
        return null;
    }
}
