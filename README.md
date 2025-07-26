# vc_
#!/bin/sh  created by 

HOST=$(hostname -s)
DATE=$(date)

# Get host totals so report can be created 
cpu_threads=$(esxcli hardware cpu list | grep "Thread Count" | awk '{sum += $NF} END {print sum}')
cpu_mhz=$(esxcli hardware cpu global get | grep "Speed" | awk '{print $3}')
mem_total_mb=$(esxcli hardware memory get | grep "Physical Memory" | awk '{print $4}')
host_total_mhz=$((cpu_threads * cpu_mhz))

echo "=== VM Resource Usage Report : $HOST ==="
echo "Generated on date: $DATE"
echo "-------------------------------------------------------------"
echo "Host CPU Threads     : $cpu_threads"
echo "Host CPU MHz Total   : $host_total_mhz MHz"
echo "Host Memory Total    : $mem_total_mb MB"
echo ""
echo ""

printf "%-25s %-6s %-8s %-10s %-12s %-12s\n" "VM Name" "vCPU" "AllocMB" "CPU MHz" "Mem Used(MB)" "PowerState"

echo "-------------------------------------------------------------------------"

# Totals
total_vcpus=0
total_mem_alloc=0
total_cpu_used=0
total_mem_used=0

for vmid in $(vim-cmd vmsvc/getallvms | awk 'NR>1 {print $1}'); do
    # Get VM info
    summary=$(vim-cmd vmsvc/get.summary $vmid)

    name=$(echo "$summary" | grep "name =" | awk -F\" '{print $2}')
    vcpus=$(echo "$summary" | grep "numCpu =" | awk '{print $3}' | tr -d ',')
    alloc_mb=$(echo "$summary" | grep "memorySizeMB =" | awk '{print $3}' | tr -d ',')
    power=$(echo "$summary" | grep "powerState =" | awk -F\" '{print $2}')

    cpu_mhz=$(echo "$summary" | grep "overallCpuUsage =" | awk '{print $3}' | tr -d ',')
    mem_mb=$(echo "$summary" | grep "guestMemoryUsage =" | awk '{print $3}' | tr -d ',')

    # Set default to 0 if Virtual machine not on
    [ -z "$cpu_mhz" ] && cpu_mhz=0
    [ -z "$mem_mb" ] && mem_mb=0

    # accumulating values
    total_vcpus=$((total_vcpus + vcpus))
    total_mem_alloc=$((total_mem_alloc + alloc_mb))
    total_cpu_used=$((total_cpu_used + cpu_mhz))
    total_mem_used=$((total_mem_used + mem_mb))

    # Print line to display those
    printf "%-25s %-6s %-8s %-10s %-12s %-12s\n" "$name" "$vcpus" "$alloc_mb" "$cpu_mhz" "$mem_mb" "$power"
done

echo "-------------------------------------------------------------------------"
echo "Total Allocated vCPUs   : $total_vcpus"
echo "Total Allocated Mem     : $total_mem_alloc MB"
echo "Total Actual CPU Usage  : $total_cpu_used MHz"
echo "Total Actual Mem Usage  : $total_mem_used MB"

cpu_usage_pct=$(awk "BEGIN {printf \"%.2f\", ($total_cpu_used/$host_total_mhz)*100}")
mem_usage_pct=$(awk "BEGIN {printf \"%.2f\", ($total_mem_used/$mem_total_mb)*100}")

echo "CPU Usage (real-time)   : $cpu_usage_pct% of total"
echo "Memory Usage (real-time): $mem_usage_pct% of total"

echo "---------------End of Host / VM resource Report-----------------------------"
