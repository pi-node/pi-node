// backend/src/main/config.js

require('dotenv').config();
const Joi = require('joi');

// Define the schema for environment variable validation
const schema = Joi.object({
    PORT: Joi.number().default(3000),
    NODE_ENV: Joi.string().valid('development', 'production', 'test').default('development'),
    PUBLIC_API_URL: Joi.string().uri().required(),
    LOG_LEVEL: Joi.string().valid('info', 'warn', 'error', 'debug').default('info'),
});

// Validate environment variables
const { error, value: validatedEnv } = schema.validate(process.env);

if (error) {
    throw new Error(`Config validation error: ${error.message}`);
}

// Export the validated configuration
module.exports = {
    PORT: validatedEnv.PORT,
    NODE_ENV: validatedEnv.NODE_ENV,
    PUBLIC_API_URL: validatedEnv.PUBLIC_API_URL,
    LOG_LEVEL: validatedEnv.LOG_LEVEL,
};
