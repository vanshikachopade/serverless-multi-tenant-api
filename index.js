const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, GetCommand, UpdateCommand } = require("@aws-sdk/lib-dynamodb");

const client = new DynamoDBClient({ region: "ap-southeast-2" });
const dynamo = DynamoDBDocumentClient.from(client);

exports.handler = async (event) => {
    try {
        // 🔐 1. AUTH CHECK
        const authHeader = event.headers?.Authorization || event.headers?.authorization;

        if (!authHeader || authHeader !== "Bearer my-secret-token") {
            return {
                statusCode: 401,
                body: JSON.stringify({
                    message: "Unauthorized ❌"
                })
            };
        }

        // 📥 2. INPUT
        const name = event.queryStringParameters?.name || "Guest";
        const tenantId = event.queryStringParameters?.tenantId || "tenant_1";

        // 🧾 3. GET TENANT CONFIG
        const tenantData = await dynamo.send(new GetCommand({
            TableName: "tenants",
            Key: { tenantId }
        }));

        if (!tenantData.Item) {
            return {
                statusCode: 404,
                body: JSON.stringify({
                    message: "Tenant not found"
                })
            };
        }

        const rateLimit = tenantData.Item.rateLimit;

        // 📊 4. GET CURRENT USAGE
        const usageData = await dynamo.send(new GetCommand({
            TableName: "Usage",
            Key: { tenantId }
        }));

        let currentCount = usageData.Item?.count || 0;

        // 🚫 5. RATE LIMIT CHECK
        if (currentCount >= rateLimit) {
            return {
                statusCode: 429,
                body: JSON.stringify({
                    message: "Rate limit exceeded ❌",
                    limit: rateLimit
                })
            };
        }

        // ➕ 6. INCREMENT USAGE
        await dynamo.send(new UpdateCommand({
            TableName: "Usage",
            Key: { tenantId },
            UpdateExpression: "SET #c = if_not_exists(#c, :start) + :inc",
            ExpressionAttributeNames: { "#c": "count" },
            ExpressionAttributeValues: {
                ":inc": 1,
                ":start": 0
            }
        }));

        // ✅ 7. SUCCESS RESPONSE
        return {
            statusCode: 200,
            body: JSON.stringify({
                message: `Hello ${name} 🚀`,
                usage: currentCount + 1,
                limit: rateLimit
            })
        };

    } catch (error) {
        console.log("ERROR:", error);

        return {
            statusCode: 500,
            body: JSON.stringify({
                error: error.message
            })
        };
    }
};