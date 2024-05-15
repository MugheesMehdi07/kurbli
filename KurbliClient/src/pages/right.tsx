export function Right({ valid_address }: any) {
  return (
    <div className="flex flex-col bg-[#18180B]">
      <div className="bg-white order-2 md:order-none">
        <img
          className=""
          src={`${valid_address ? "/valid.png" : "/home.png"}`}
          height="600px"
          width="1200px"
        />
      </div>

      <div className="mx-3 md:mx-2 my-4 md:my-2 p-0 md:p-2 order-1 md:order-none">
        <h2 className="text-lg sm:text-2xl md:leading-[32px] text-white">
          How does kurbli work?
        </h2>

        <p className="text-xs sm:text-base text-white mt-3 sm:mt-6">
          kurbli uses a proprietary combination of artificial intelligence and
          predictive analytics to determine how investible your property may be
          to potential investors.
        </p>
      </div>
      {/* <div className="text-2xl font-semibold text-gray-300 m-2 p-2">
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
      </div> */}
    </div>
  );
}
