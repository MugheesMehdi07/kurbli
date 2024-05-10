import { ReactBatchAutocomplete } from "@batchservice/react-batch-autocomplete-lib";

export function Suggestion({ onClick }: any) {
  const recentSearch = [
    // { name: "123 Dora Ln, Byron, GA 31008" },
    // { name: "123 Manor Way, Hendersonville, TN 37075" },
    // { name: "434 Bourbon Ave, Lexington, KY 40508" },
    {},
  ];

  const handleError = (e: any) => {
    console.log("Error while searching: ", e);
  };

  const onSelect = (data: any) => {
    onClick(data);
  };

  const suggestionList = (data: any) => {
    console.log(data);
    onClick(data);
  };

  return (
    <div>
      <ReactBatchAutocomplete
        placeholder="Start typing to select the address"
        notFoundText="Not found data"
        debounce={700}
        apiKey="MDBUSyko3Q2cpXho7NboEIEzAaAKncCw9AIbTfbZ"
        domainServer="https://api.batchdata.com/api/v1/address/autocomplete"
        recentSearch={recentSearch}
        handleError={(e: any) => handleError(e)}
        suggestionList={(data: any) => suggestionList(data)}
        onSelect={(data: any) => onSelect(data)}
        displayData="name"
        showNotFound={true}
        take={5}
        filterType={[]}
      />
    </div>
  );
}
