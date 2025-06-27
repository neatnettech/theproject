import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { StagingChange } from "../types";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { StagingTitle } from "@repo/ui";

export default function Home() {
  const [changes, setChanges] = useState<StagingChange[]>([]);
  const [loading, setLoading] = useState(true);
  const [backendOk, setBackendOk] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChanges = async () => {
      try {
        const res = await fetch(
          "http://127.0.0.1:8000/api/v1/staging/changes"
        );
        if (res.ok) {
          const json = await res.json();
          setChanges(json.changes);
          setBackendOk(true);
        }
      } catch (err) {
        console.error("Backend check failed:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchChanges();
  }, []);

  const handleAction = (id: number, action: string) => {
    console.log(`Action "${action}" taken on row ID ${id}`);
    // optionally: trigger backend call here
  };

  const columns: ColumnDef<StagingChange>[] = [
    { header: "ID", accessorKey: "id" },
    { header: "Changeset", accessorKey: "changeset_id" },
    { header: "Record ID", accessorKey: "record_id" },
    { header: "Action", accessorKey: "action" },
    { header: "Status", accessorKey: "status" },
    { header: "Source", accessorKey: "change_source" },
    { header: "Justification", accessorKey: "business_justification" },
    { header: "Directory", accessorKey: "directory" },
    { header: "Created By", accessorKey: "created_by" },
    {
      header: "Created At",
      accessorKey: "created_at",
      cell: (info) => new Date(info.getValue<string>()).toLocaleString(),
    },
    {
      header: "",
      id: "actions",
      cell: ({ row }) => {
        const rowId = row.original.id;
        return (
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <button
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                }}
                title="Actions"
              >
                ⋮
              </button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content
              sideOffset={4}
              style={{
                background: "white",
                border: "1px solid #ccc",
                borderRadius: 4,
                padding: "0.5rem",
                zIndex: 1000,
              }}
            >
              <DropdownMenu.Item
                onSelect={() =>
                  navigate(
                    `/details/${row.original.changeset_id}/${row.original.record_id}`
                  )
                }
              >
                🔍 View Details
              </DropdownMenu.Item>
              <DropdownMenu.Item onSelect={() => handleAction(rowId, "accept")}>
                ✅ Accept
              </DropdownMenu.Item>
              <DropdownMenu.Item onSelect={() => handleAction(rowId, "reject")}>
                ❌ Reject
              </DropdownMenu.Item>
              <DropdownMenu.Item onSelect={() => handleAction(rowId, "review")}>
                👀 Review
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        );
      },
    },
  ];

  const table = useReactTable({
    data: changes,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Staging Table</h1>
      <StagingTitle>
        Test
      </StagingTitle>

      {loading && <p>Checking backend...</p>}
      {!loading && backendOk && (
        <p style={{ color: "green" }}>✅ Backend is working</p>
      )}
      {!loading && !backendOk && (
        <p style={{ color: "red" }}>❌ Backend not reachable</p>
      )}

      {!loading && changes.length > 0 && (
        <table
          border={1}
          cellPadding={6}
          style={{
            marginTop: "1rem",
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id}>
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
