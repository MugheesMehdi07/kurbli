import { Input } from "../UI/input_box";

export function LeftText({
  toggleScoreBadge,
  setKurbilScore,
  kurbilScore,
  setValid_address,
  valid_address,
  score,
  setScore,
}: any) {
  return (
    <div
      className={`flex flex-col items-start justify-start p-0 md:p-4 lg:p-16 m-4 ${
        valid_address
          ? "2xl:m-[40px_0px_40px_40px]"
          : "2xl:m-[40px_150px_40px_40px]"
      } order-1 md:order-none`}
    >
      <div className={`${valid_address ? "mr-0 lg:mr-20 2xl:mr-32" : ""}`}>
        <h2 className="text-xl lg:text-[36px] leading-7 lg:leading-[50px] text-[#18180B] font-semibold">
          {valid_address
            ? score
              ? "Congratulations! Your home has GREAT kurbli appeal!"
              : "Enter your property address and get your kurbli score."
            : "Get your kurbli score and see how appealing your home could be to investors."}
        </h2>
        <p className="text-sm lg:text-base text-[#696969] font-normal mt-2 lg:mt-4">
          {valid_address
            ? score
              ? "Knowing your kurbli score lets you value your home the same way an investor might. Feel free to brag - your property deserves it!"
              : "Enter your property address and get your kurbli score."
            : " Get started by entering your email address below."}
        </p>
      </div>
      <div className="mt-5 sm:mt-14 w-full">
        <Input
          toggleScoreBadge={toggleScoreBadge}
          fn={setKurbilScore}
          final_score={kurbilScore}
          setValid_address={setValid_address}
          valid_address={valid_address}
          score={score}
          setScore={setScore}
        />
      </div>
    </div>
  );
}
