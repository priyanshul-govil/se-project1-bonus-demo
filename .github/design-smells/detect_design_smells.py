import os
import openai


# Assuming your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def apply_refactoring(file_path, refactored_code):
    """Replace the content of the file with refactored code."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(refactored_code)


def analyze_and_refactor_smells(file_path):
    """Send the content of the given file to the OpenAI API to detect design smells."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    """Get design smells"""
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {
            "role": "system",
            "content": "You are a software engineer working to refactor a GitHub repository by identifying design smells."
            },
            {
            "role": "user",
            "content": f"Identify design smells in the file, and suggest refactoring changes. Be precise and concise. List only (1) Identified Design Smells, and (2) Suggested Refactoring.\n\nf{code_content}"
            }
        ],
        temperature=0.8,
        max_tokens=1200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    smells = response.choices[0].message.content
    print(smells)

    """Get refactored code"""
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are a software engineer working to refactor a GitHub repository by identifying design smells."
        },
        {
        "role": "user",
        "content": "Identify design smells in the file, and suggest refactoring changes. Be precise and concise. List only (1) Identified Design Smells, and (2) Suggested Refactoring.\n\npackage com.sismics.books.rest.resource;\n\nimport java.util.ArrayList;\nimport java.util.List;\nimport java.util.ResourceBundle;\n\nimport javax.ws.rs.FormParam;\nimport javax.ws.rs.GET;\nimport javax.ws.rs.POST;\nimport javax.ws.rs.Path;\nimport javax.ws.rs.Produces;\nimport javax.ws.rs.QueryParam;\nimport javax.ws.rs.core.MediaType;\nimport javax.ws.rs.core.Response;\n\nimport org.apache.commons.lang.StringUtils;\nimport org.apache.log4j.Appender;\nimport org.apache.log4j.Logger;\nimport org.codehaus.jettison.json.JSONException;\nimport org.codehaus.jettison.json.JSONObject;\n\nimport com.sismics.books.core.constant.ConfigType;\nimport com.sismics.books.core.dao.jpa.ConfigDao;\nimport com.sismics.books.core.model.context.AppContext;\nimport com.sismics.books.core.util.ConfigUtil;\nimport com.sismics.books.core.util.jpa.PaginatedList;\nimport com.sismics.books.core.util.jpa.PaginatedLists;\nimport com.sismics.books.rest.constant.BaseFunction;\nimport com.sismics.rest.exception.ForbiddenClientException;\nimport com.sismics.rest.exception.ServerException;\nimport com.sismics.rest.util.ValidationUtil;\nimport com.sismics.util.log4j.LogCriteria;\nimport com.sismics.util.log4j.LogEntry;\nimport com.sismics.util.log4j.MemoryAppender;\n\n/**\n * General app REST resource.\n * \n * @author jtremeaux\n */\n@Path(\"/app\")\npublic class AppResource extends BaseResource {\n    /**\n     * Return the information about the application.\n     * \n     * @return Response\n     * @throws JSONException\n     */\n    @GET\n    @Produces(MediaType.APPLICATION_JSON)\n    public Response info() throws JSONException {\n        if (!authenticate()) {\n            throw new ForbiddenClientException();\n        }\n        \n        ResourceBundle configBundle = ConfigUtil.getConfigBundle();\n        String currentVersion = configBundle.getString(\"api.current_version\");\n        String minVersion = configBundle.getString(\"api.min_version\");\n\n        JSONObject response = new JSONObject();\n        \n        // General data\n        response.put(\"current_version\", currentVersion.replace(\"-SNAPSHOT\", \"\"));\n        response.put(\"min_version\", minVersion);\n        response.put(\"total_memory\", Runtime.getRuntime().totalMemory());\n        response.put(\"free_memory\", Runtime.getRuntime().freeMemory());\n        \n        // Specific data\n        response.put(\"api_key_google\", ConfigUtil.getConfigStringValue(ConfigType.API_KEY_GOOGLE));\n        \n        return Response.ok().entity(response).build();\n    }\n    \n    /**\n     * Update application configuration.\n     * \n     * @return Response\n     * @throws JSONException\n     */\n    @POST\n    @Produces(MediaType.APPLICATION_JSON)\n    public Response update(\n            @FormParam(\"api_key_google\") String apiKeyGoogle) throws JSONException {\n        if (!authenticate()) {\n            throw new ForbiddenClientException();\n        }\n        checkBaseFunction(BaseFunction.ADMIN);\n        \n        // Validate input data\n        apiKeyGoogle = ValidationUtil.validateLength(apiKeyGoogle, \"api_key_google\", 1, 250, false);\n        \n        ConfigDao configDao = new ConfigDao();\n        configDao.getById(ConfigType.API_KEY_GOOGLE).setValue(apiKeyGoogle);\n        \n        AppContext.getInstance().getBookDataService().initConfig();\n        \n        JSONObject response = new JSONObject();\n        response.put(\"status\", \"ok\");\n        return Response.ok().entity(response).build();\n    }\n    \n    /**\n     * Retrieve the application logs.\n     * \n     * @param level Filter on logging level\n     * @param tag Filter on logger name / tag\n     * @param message Filter on message\n     * @param limit Page limit\n     * @param offset Page offset\n     * @return Response\n     * @throws JSONException\n     */\n    @GET\n    @Path(\"log\")\n    @Produces(MediaType.APPLICATION_JSON)\n    public Response log(\n            @QueryParam(\"level\") String level,\n            @QueryParam(\"tag\") String tag,\n            @QueryParam(\"message\") String message,\n            @QueryParam(\"limit\") Integer limit,\n            @QueryParam(\"offset\") Integer offset) throws JSONException {\n        if (!authenticate()) {\n            throw new ForbiddenClientException();\n        }\n        checkBaseFunction(BaseFunction.ADMIN);\n\n        // Get the memory appender\n        Logger logger = Logger.getRootLogger();\n        Appender appender = logger.getAppender(\"MEMORY\");\n        if (!(appender instanceof MemoryAppender)) {\n            throw new ServerException(\"ServerError\", \"MEMORY appender not configured\");\n        }\n        MemoryAppender memoryAppender = (MemoryAppender) appender;\n        \n        // Find the logs\n        LogCriteria logCriteria = new LogCriteria();\n        logCriteria.setLevel(StringUtils.stripToNull(level));\n        logCriteria.setTag(StringUtils.stripToNull(tag));\n        logCriteria.setMessage(StringUtils.stripToNull(message));\n        \n        PaginatedList<LogEntry> paginatedList = PaginatedLists.create(limit, offset);\n        memoryAppender.find(logCriteria, paginatedList);\n        JSONObject response = new JSONObject();\n        List<JSONObject> logs = new ArrayList<>();\n        for (LogEntry logEntry : paginatedList.getResultList()) {\n            JSONObject log = new JSONObject();\n            log.put(\"date\", logEntry.getTimestamp());\n            log.put(\"level\", logEntry.getLevel());\n            log.put(\"tag\", logEntry.getTag());\n            log.put(\"message\", logEntry.getMessage());\n            logs.add(log);\n        }\n        response.put(\"total\", paginatedList.getResultCount());\n        response.put(\"logs\", logs);\n        \n        return Response.ok().entity(response).build();\n    }\n}"
        },
        {
        "role": "assistant",
        "content": "(1) Identified Design Smells:\n\na. Large Class: The class `AppResource` seems to handle many responsibilities (methods `info`, `update`, `log`). This is a violation of the Single Responsibility Principle.\n\nb. Long Method: The methods `info`, `update`, `log` in the `AppResource` class are quite lengthy. This makes it harder to understand and maintain.\n\nc. Inappropriate Intimacy: The `AppResource` class seems to directly use and manipulate many other classes such as `ConfigDao`, `AppContext`, `MemoryAppender`, etc. This is a type of coupling that can make the system harder to modify.\n\nd. Data Class: The `LogEntry` class is likely a data class as it only contains data and no behavior.\n\n(2) Suggested Refactoring:\n\na. Extract Class: Divide the responsibilities of the `AppResource` class into multiple classes. For example, create separate classes like `AppInfoResource`, `AppUpdateResource`, and `AppLogResource`.\n\nb. Extract Method: Break down the lengthy methods (`info`, `update`, `log`) into smaller ones with clear, descriptive names.\n\nc. Move Method / Hide Method: Encapsulate the manipulation of classes such as `ConfigDao`, `AppContext`, `MemoryAppender` etc. inside their own classes. This reduces the coupling between these classes and `AppResource`.\n\nd. For `LogEntry`, if it's indeed just a data class, it might be appropriate to add any behavior associated with a log entry to this class. This would transform it from a passive data class to a more active one that encapsulates its own behavior."
        },
        {
        "role": "user",
        "content": "Provide a refactored code based on your suggestions. If any refactoring requires modification of external files, skip it. Provide the entire code without any assumptions. Do not include anything apart from the code, as the code would be copy-pasted for testing purposes."
        },
    ],
    temperature=1,
    max_tokens=5034,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    refactored_code = response.choices[0].message.content
    # Code is between ``` and ``` in the response. Keep only that part.
    refactored_code = refactored_code.split("```")[1]

    # Apply refactoring
    apply_refactoring(file_path, refactored_code)


def main(directory):
    """Iterate over all Python files in the directory, analyze them for design smells, and attempt refactoring."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                
                # Detect and refactor design smells
                analyze_and_refactor_smells(file_path)

                # Testing purposes: exit after processing one file
                exit()

if __name__ == "__main__":
    directory_to_analyze = "."
    main(directory_to_analyze)
