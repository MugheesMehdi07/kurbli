export function Checkbox({ setIsChecked, isChecked }: any) {
  return (
    <div className="flex items-center pt-2 pb-5 lg:py-5">
      <div
        className="bg-white w-5 lg:w-[30px] h-5 lg:h-[30px] border border-[#494949] rounded lg:rounded-md p-1 flex justify-center items-center mr-0 lg:mr-2"
        onClick={() => setIsChecked((prev: any) => !prev)}
      >
        <input type="checkbox" className="hidden" checked />
        <svg
          className={`${isChecked ? "" : "hidden"} w-5 h-5 pointer-events-none`}
          viewBox="0 0 172 172"
        >
          <g
            fill="none"
            stroke-width="none"
            stroke-miterlimit="10"
            font-family="none"
            font-weight="none"
            font-size="none"
            text-anchor="none"
            style={{ mixBlendMode: "normal" }}
          >
            <path d="M0 172V0h172v172z" />
            <path
              d="M145.433 37.933L64.5 118.8658 33.7337 88.0996l-10.134 10.1341L64.5 139.1341l91.067-91.067z"
              fill="currentColor"
              stroke-width="1"
            />
          </g>
        </svg>
      </div>
      <label className="w-full lg:w-[60%] ms-2 text-[13px] leading-[18px] font-normal text-[#494949] text-justify lg:text-start">
        By checking the box, you agree allow us to use your information to
        contact you about our services.
      </label>
    </div>
  );
}
