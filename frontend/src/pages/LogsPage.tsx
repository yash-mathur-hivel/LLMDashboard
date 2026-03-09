import { useState } from "react";
import { Topbar } from "@/components/layout/Topbar";
import { LogTable } from "@/components/logs/LogTable";
import { LogFilters } from "@/components/logs/LogFilters";
import { LogDetailPanel } from "@/components/logs/LogDetailPanel";
import { useLogs } from "@/hooks/useLogs";
import { useDimensions } from "@/hooks/useAnalytics";
import type { LogFilters as LogFiltersType } from "@/types/log";
import { ChevronLeft, ChevronRight, RefreshCw } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";

export function LogsPage() {
  const qc = useQueryClient();
  const [filters, setFilters] = useState<LogFiltersType>({ page: 1, page_size: 50 });
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const { data, isLoading, isFetching } = useLogs(filters);
  const { data: dimensions } = useDimensions();

  const setPage = (p: number) => setFilters((f) => ({ ...f, page: p }));

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <Topbar
        title="Request Logs"
        actions={
          <button
            onClick={() => qc.invalidateQueries({ queryKey: ["logs"] })}
            className="text-[#475569] hover:text-white transition-colors"
          >
            <RefreshCw size={15} className={isFetching ? "animate-spin" : ""} />
          </button>
        }
      />

      <LogFilters filters={filters} dimensions={dimensions} onChange={setFilters} />

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 flex flex-col overflow-hidden">
          {isLoading ? (
            <div className="flex-1 flex items-center justify-center text-[#475569] text-sm">
              Loading…
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto">
              <LogTable
                items={data?.items ?? []}
                selectedId={selectedId}
                onSelect={setSelectedId}
              />
            </div>
          )}

          {/* Pagination */}
          {data && data.total_pages > 1 && (
            <div className="border-t border-[#1e293b] px-4 py-2 flex items-center justify-between text-xs text-[#475569]">
              <span>
                {data.total} total · page {data.page} of {data.total_pages}
              </span>
              <div className="flex items-center gap-1">
                <button
                  disabled={data.page <= 1}
                  onClick={() => setPage(data.page - 1)}
                  className="p-1 disabled:opacity-30 hover:text-white transition-colors"
                >
                  <ChevronLeft size={14} />
                </button>
                <button
                  disabled={data.page >= data.total_pages}
                  onClick={() => setPage(data.page + 1)}
                  className="p-1 disabled:opacity-30 hover:text-white transition-colors"
                >
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          )}
        </div>

        {selectedId && (
          <LogDetailPanel logId={selectedId} onClose={() => setSelectedId(null)} />
        )}
      </div>
    </div>
  );
}
