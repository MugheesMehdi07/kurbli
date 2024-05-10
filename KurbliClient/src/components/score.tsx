export function Score({ text, color }: { text: any; color: string }) {
  return (
    <div className="px-1 mb-2 mr-2" style={{ whiteSpace: "nowrap" }}>
      <div
        className="px-2 py-2 rounded-full font-semibold"
        style={{ backgroundColor: color }}
      >
        {text}
      </div>
    </div>
  );
}
