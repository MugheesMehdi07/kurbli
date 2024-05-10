export function Right() {
  return (
    <div className="bg-black">
      <div className="bg-white">
        <img className="" src="/home.png" height="600px" width="1200px" />
      </div>

      <div className="text-2xl font-semibold text-gray-300 m-2 p-2">
        What is Krubli's real-time scoring system?
      </div>
      <div className="text-gray-300 m-2 p-2">
        Krubli's real-time scoring system is a tool designed for homeowners to
        assess how applealing their property is to potenial investors based on
        various factors
      </div>
      <div className="text-2xl font-semibold text-gray-300 m-2 p-2">
        What we provide
      </div>
      <div className="flex p-2 m-2">
        <div className="flex flex-col text-gray-300 p-1 m-1">
          <img src="/threelines.svg" width="56px" height="56px" />
          <div className="m-1">Listing your home for sale</div>
        </div>
        <div className="flex flex-col text-gray-300 p-1 m-1">
          <img src="/search.svg" width="56px" height="56px" />
          <div className="m-1">Finding homes for you to buy</div>
        </div>
        <div className="flex flex-col text-gray-300 p-1 m-1">
          <img src="bucket.svg" width="56px" height="56px" />
          <div className="m-1">Providing you with market information</div>
        </div>
        <div className="flex flex-col text-gray-300 p-1 m-1">
          <img src="dollar.svg" width="56px" height="56px" />
          <div className="m-1">Negotiating on your behalf</div>
        </div>
      </div>
    </div>
  );
}
