const REPO = 'Frontend'
const OWNER = 'SwiftPix'
const SONAR_ID = 'SwiftPix_User-service'

const METRIC_LIST = [
    'files',
    'functions',
    'complexity',
    'comment_lines_density',
    'duplicated_lines_density',
    'coverage',
    'ncloc',
    'tests',
    'test_errors',
    'test_failures',
    'test_execution_time',
    'security_rating'
];

const SONAR_URL = `https://sonarcloud.io/api/measures/component_tree?component=${SONAR_ID}&metricKeys=${METRIC_LIST.join(',')}&ps=500`;

module.exports = {
    SONAR_URL,
    REPO,
    OWNER
};