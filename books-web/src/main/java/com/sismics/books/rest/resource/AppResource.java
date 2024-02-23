java
package com.sismics.books.rest.resource;

import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.commons.lang.StringUtils;
import org.apache.log4j.Appender;
import org.apache.log4j.Logger;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;

import com.sismics.books.core.constant.ConfigType;
import com.sismics.books.core.dao.jpa.ConfigDao;
import com.sismics.books.core.model.context.AppContext;
import com.sismics.books.core.util.ConfigUtil;
import com.sismics.books.core.util.jpa.PaginatedList;
import com.sismics.books.core.util.jpa.PaginatedLists;
import com.sismics.books.rest.constant.BaseFunction;
import com.sismics.rest.exception.ForbiddenClientException;
import com.sismics.rest.exception.ServerException;
import com.sismics.rest.util.ValidationUtil;
import com.sismics.util.log4j.LogCriteria;
import com.sismics.util.log4j.LogEntry;
import com.sismics.util.log4j.MemoryAppender;

@Path("/app")
public class AppResource extends BaseResource {

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response info() throws JSONException {
        checkAuthentication();
        
        JSONObject response = formInfoJsonResponse();
        
        return Response.ok().entity(response).build();
    }

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    public Response update(@FormParam("api_key_google") String apiKeyGoogle) throws JSONException {
        checkAuthentication();
        checkBaseFunction(BaseFunction.ADMIN);
        
        updateConfig(apiKeyGoogle);
        
        JSONObject response = new JSONObject();
        response.put("status", "ok");
        return Response.ok().entity(response).build();
    }

    @GET
    @Path("log")
    @Produces(MediaType.APPLICATION_JSON)
    public Response log(@QueryParam("level") String level,
                        @QueryParam("tag") String tag,
                        @QueryParam("message") String message,
                        @QueryParam("limit") Integer limit,
                        @QueryParam("offset") Integer offset) throws JSONException {
        checkAuthentication();
        checkBaseFunction(BaseFunction.ADMIN);

        MemoryAppender memoryAppender = getAppender();
        
        PaginatedList<LogEntry> paginatedList = findLogs(level, tag, message, memoryAppender, limit, offset);
        
        JSONObject response = createLogJsonResponse(paginatedList);

        return Response.ok().entity(response).build();
    }

    private void checkAuthentication() {
        if (!authenticate()) {
            throw new ForbiddenClientException();
        }
    }

    private JSONObject formInfoJsonResponse() throws JSONException {
        ResourceBundle configBundle = ConfigUtil.getConfigBundle();
        String currentVersion = configBundle.getString("api.current_version");
        String minVersion = configBundle.getString("api.min_version");

        JSONObject response = new JSONObject();
        response.put("current_version", currentVersion.replace("-SNAPSHOT", ""));
        response.put("min_version", minVersion);
        response.put("total_memory", Runtime.getRuntime().totalMemory());
        response.put("free_memory", Runtime.getRuntime().freeMemory());
        response.put("api_key_google", ConfigUtil.getConfigStringValue(ConfigType.API_KEY_GOOGLE));
        
        return response;
    }

    private void updateConfig(String apiKeyGoogle) {
        apiKeyGoogle = ValidationUtil.validateLength(apiKeyGoogle, "api_key_google", 1, 250, false);
        
        ConfigDao configDao = new ConfigDao();
        configDao.getById(ConfigType.API_KEY_GOOGLE).setValue(apiKeyGoogle);
        
        AppContext.getInstance().getBookDataService().initConfig();
    }
    
    private MemoryAppender getAppender() {
        Logger logger = Logger.getRootLogger();
        Appender appender = logger.getAppender("MEMORY");
        if (!(appender instanceof MemoryAppender)) {
            throw new ServerException("ServerError", "MEMORY appender not configured");
        }
        return (MemoryAppender) appender;
    }

    private PaginatedList<LogEntry> findLogs(String level, String tag, String message, 
                                            MemoryAppender memoryAppender, Integer limit, 
                                            Integer offset) {
        LogCriteria logCriteria = new LogCriteria();
        logCriteria.setLevel(StringUtils.stripToNull(level));
        logCriteria.setTag(StringUtils.stripToNull(tag));
        logCriteria.setMessage(StringUtils.stripToNull(message));
        
        PaginatedList<LogEntry> paginatedList = PaginatedLists.create(limit, offset);
        memoryAppender.find(logCriteria, paginatedList);

        return paginatedList;
    }

    private JSONObject createLogJsonResponse(PaginatedList<LogEntry> paginatedList) throws JSONException {
        JSONObject response = new JSONObject();
        List<JSONObject> logs = new ArrayList<>();
        for (LogEntry logEntry : paginatedList.getResultList()) {
            JSONObject log = new JSONObject();
            log.put("date", logEntry.getTimestamp());
            log.put("level", logEntry.getLevel());
            log.put("tag", logEntry.getTag());
            log.put("message", logEntry.getMessage());
            logs.add(log);
        }
        response.put("total", paginatedList.getResultCount());
        response.put("logs", logs);

        return response;
    }
}
