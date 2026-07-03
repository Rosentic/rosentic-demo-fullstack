export type StatusTone = "green" | "amber" | "red";

export function renderStatusWidget(label: string, tone: StatusTone): string {
  return `<span class="status status-${tone}">${label}</span>`;
}
