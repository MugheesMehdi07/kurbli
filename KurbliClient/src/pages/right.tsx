export function Right(){
    return(
        <div className="bg-black h-full">
            <div>
                <img className="" src="/home.jpeg" height="697px" width="1200px"/>
            </div>
            <div className="text-2xl font-semibold text-gray-300 m-2 p-4">What we provide</div>
            <div className="flex p-2 m-2">
                <div className="flex flex-col text-gray-300 p-1 m-1">
                    <img src="/threelines.svg" width="56px" height="56px"/>
                    <div className="m-1">Listing your home for sale</div>
                </div>
                <div className="flex flex-col text-gray-300 p-1 m-1">
                    <img src="/search.svg" width="56px" height="56px"/>
                    <div className="m-1">Finding homes for you to buy</div>
                </div>
                <div className="flex flex-col text-gray-300 p-1 m-1">
                    <img src="bucket.svg" width="56px" height="56px"/>
                    <div className="m-1">Providing you with market information</div>
                </div>
                <div className="flex flex-col text-gray-300 p-1 m-1">
                    <img src="dollar.svg" width="56px" height="56px"/>
                    <div className="m-1">Negotiating on your behalf</div>
                </div>
            </div>
        </div>
    )
}