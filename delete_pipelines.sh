# this script removes old GitLab CI pipelines
# there is no option to bulk delete pipelines

if [[ -z "${PROJECT_ID}" ]]; then
  echo "Please set a PROJECT_ID environment variable."
  exit 1;
fi

if [[ -z "${GITLAB_TOKEN}" ]]; then
  echo "Please set a GITLAB_TOKEN environment variable."
  exit 1;
fi



BASE_URL="https://gitlab.com/api/v4/projects/$PROJECT_ID/"
PIPELINES_URL="${BASE_URL}pipelines?private_token=$GITLAB_TOKEN&per_page=10000"


echo $PIPELINES_URL
echo "Fetching pipeline ids"
curl $PIPELINES_URL | jq -r '.[].id' > /tmp/ids.txt

echo "Deleting pipelines..."

while read l; do
    echo "Deleting $l";
    echo $l;
    sleep 1;
    output=$(curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --request "DELETE" "${BASE_URL}pipelines/$l" | echo $1);
    echo $output
    echo "Deleted pipeline $l"
done < /tmp/ids.txt
