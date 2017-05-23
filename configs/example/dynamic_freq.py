import m5
from m5.objects import *

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1MHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = AtomicSimpleCPU()
system.cpu.freq_high = "1MHz"
system.cpu.freq_low = "1MHz"
system.cpu.energy_consumed_per_cycle = 1.5
system.cpu.poweroff_panelty = 5000

system.energy_mgmt = EnergyMgmt(path_energy_profile = 'profile/energy_prof',
                                energy_time_unit = '10us')
system.energy_mgmt.state_machine = DynamicFreqSM()
system.energy_mgmt.state_machine.thres_poweron = 20000
system.energy_mgmt.state_machine.thres_poweroff = 10000
system.energy_mgmt.state_machine.thres_convert = 20000

system.cpu.s_energy_port = system.energy_mgmt.m_energy_port

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

system.cpu.createInterruptController()

system.mem_ctrl = DDR3_1600_x64()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

system.system_port = system.membus.slave

process = LiveProcess()
process.cmd = ['tests/test-progs/queens']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print "Beginning simulation!"
exit_event = m5.simulate()
print 'Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause())
