export function Navbar() {
  return (
    <div
      className="shadow-md h-16 items-center flex justify-start cursor-pointer ps-0 md:ps-4 lg:ps-10"
      onClick={() => {
        window.location.reload();
      }}
    >
      <img
        className="p-2 m-2"
        src="/logo.png"
        width="80px"
        height="20px"
      ></img>
    </div>
  );
}
