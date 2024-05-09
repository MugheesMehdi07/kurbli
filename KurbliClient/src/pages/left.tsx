import { Input } from "../componets/input_box";
import { Social_links } from "../componets/social";

export function LeftText() {
  return (
    <div className="flex flex-col items-start justify-start p-4 m-4 sm:p-10 sm:m-10">
      <div className="font-semibold text-4xl leading-[50px]">
        Start Exploring by Entering the Address
      </div>
      <div className="text-gray-600 py-4">
        Lorem ipsum dolor sit amet consectetur. In dolor lacus turpis convallis
        odio tincidunt turpis ac tristique. Velit sit ultricies tortor.
      </div>
      <Social_links />
      <Input />
    </div>
  );
}
