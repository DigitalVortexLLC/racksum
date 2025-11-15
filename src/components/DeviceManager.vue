<template>
  <div
    class="modal modal-open"
    @click.self="$emit('close')"
  >
    <div class="modal-box w-full max-w-5xl max-h-[90vh] flex flex-col p-0 shadow-2xl">
      <!-- Header -->
      <div class="relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-br from-primary to-primary-focus opacity-90" />
        <div class="relative flex items-center justify-between p-8">
          <div>
            <h2 class="text-3xl font-bold text-primary-content mb-1">
              Device Manager
            </h2>
            <p class="text-primary-content/70 text-sm">
              Manage groups, devices, and resources
            </p>
          </div>
          <button
            class="btn btn-ghost btn-circle text-primary-content hover:bg-primary-content/20"
            @click="$emit('close')"
          >
            <svg
              class="size-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <div class="flex-1 overflow-hidden flex flex-col bg-base-100">
        <!-- Tab Navigation -->
        <div
          role="tablist"
          class="tabs tabs-boxed mx-6 mt-6 mb-4 bg-base-200 p-1 gap-1"
        >
          <button
            role="tab"
            class="tab flex-1 transition-all duration-200"
            :class="activeTab === 'groups' ? 'tab-active bg-primary text-primary-content shadow-md' : 'hover:bg-base-300'"
            @click="activeTab = 'groups'"
          >
            <svg
              class="size-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            Groups
          </button>
          <button
            role="tab"
            class="tab flex-1 transition-all duration-200"
            :class="activeTab === 'devices' ? 'tab-active bg-primary text-primary-content shadow-md' : 'hover:bg-base-300'"
            @click="activeTab = 'devices'"
          >
            <svg
              class="size-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"
              />
            </svg>
            Devices
          </button>
          <button
            role="tab"
            class="tab flex-1 transition-all duration-200"
            :class="activeTab === 'providers' ? 'tab-active bg-primary text-primary-content shadow-md' : 'hover:bg-base-300'"
            @click="activeTab = 'providers'"
          >
            <svg
              class="size-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            Providers
          </button>
          <button
            role="tab"
            class="tab flex-1 transition-all duration-200"
            :class="activeTab === 'import-export' ? 'tab-active bg-primary text-primary-content shadow-md' : 'hover:bg-base-300'"
            @click="activeTab = 'import-export'"
          >
            <svg
              class="size-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
              />
            </svg>
            Import/Export
          </button>
        </div>

        <!-- Device Groups Tab -->
        <div
          v-if="activeTab === 'groups'"
          class="flex-1 overflow-y-auto px-6 pb-6"
        >
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-lg font-semibold">
                Device Groups
              </h3>
              <p class="text-sm opacity-70">
                Organize devices into categories
              </p>
            </div>
            <button
              class="btn btn-primary gap-2"
              @click="addGroupDialog?.showModal()"
            >
              <svg
                class="size-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add Group
            </button>
          </div>

          <div class="grid gap-3">
            <div
              v-for="group in deviceGroups"
              :key="group.id"
              class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-200 border border-base-300"
            >
              <div class="card-body p-4 flex flex-row items-center gap-4">
                <div
                  class="w-16 h-16 rounded-lg flex-shrink-0 shadow-inner"
                  :style="{ backgroundColor: group.color }"
                />
                <div class="flex-1 min-w-0">
                  <h4 class="card-title text-base mb-1">
                    {{ group.name }}
                  </h4>
                  <div class="flex items-center gap-2 text-sm opacity-70">
                    <span class="badge badge-ghost badge-sm">{{ group.deviceCount || 0 }} devices</span>
                    <span class="text-xs">•</span>
                    <span class="text-xs">{{ group.color }}</span>
                  </div>
                </div>
                <div class="card-actions flex-shrink-0">
                  <button
                    class="btn btn-ghost btn-sm btn-square hover:btn-primary"
                    title="Edit group"
                    @click="editGroup(group)"
                  >
                    <svg
                      class="size-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    class="btn btn-ghost btn-sm btn-square hover:btn-error"
                    title="Delete group"
                    @click="deleteGroup(group.id)"
                  >
                    <svg
                      class="size-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Devices Tab -->
        <div
          v-if="activeTab === 'devices'"
          class="flex-1 overflow-y-auto px-6 pb-6"
        >
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-lg font-semibold">
                Custom Devices
              </h3>
              <p class="text-sm opacity-70">
                Create and manage your device library
              </p>
            </div>
            <button
              class="btn btn-primary gap-2"
              @click="addDeviceDialog?.showModal()"
            >
              <svg
                class="size-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add Device
            </button>
          </div>

          <div class="grid gap-3">
            <div
              v-for="device in customDevices"
              :key="device.id"
              class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-200 border border-base-300"
            >
              <div class="card-body p-4 flex flex-row items-center gap-4">
                <div
                  class="w-20 h-20 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-lg flex-shrink-0"
                  :style="{ backgroundColor: device.color }"
                >
                  {{ device.ruSize }}U
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="card-title text-base mb-2">
                    {{ device.name }}
                  </h4>
                  <div class="flex flex-wrap gap-2 mb-2">
                    <span class="badge badge-primary badge-sm">{{ device.category }}</span>
                    <span class="badge badge-ghost badge-sm">{{ device.ruSize }}U</span>
                    <span class="badge badge-ghost badge-sm">{{ device.powerDraw }}W</span>
                    <span class="badge badge-ghost badge-sm">{{ device.powerPortsUsed || 1 }} port(s)</span>
                  </div>
                  <p
                    v-if="device.description"
                    class="text-xs opacity-70 line-clamp-2"
                  >
                    {{ device.description }}
                  </p>
                </div>
                <div class="card-actions flex-shrink-0 flex flex-col gap-1">
                  <button
                    class="btn btn-ghost btn-xs btn-square hover:btn-info"
                    title="Duplicate device"
                    @click="duplicateDevice(device)"
                  >
                    <svg
                      class="size-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                  </button>
                  <button
                    class="btn btn-ghost btn-xs btn-square hover:btn-primary"
                    title="Edit device"
                    @click="editDevice(device)"
                  >
                    <svg
                      class="size-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    class="btn btn-ghost btn-xs btn-square hover:btn-error"
                    title="Delete device"
                    @click="deleteDevice(device.id)"
                  >
                    <svg
                      class="size-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Resource Providers Tab -->
        <div
          v-if="activeTab === 'providers'"
          class="flex-1 overflow-y-auto px-6 pb-6"
        >
          <div class="alert alert-info mb-6 shadow-md">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              class="stroke-current shrink-0 w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div>
              <h3 class="font-bold">
                About Resource Providers
              </h3>
              <div class="text-sm">
                Infrastructure components that add capacity to your site (PDUs, HVAC units, network uplinks, etc.)
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-lg font-semibold">
                Resource Providers
              </h3>
              <p class="text-sm opacity-70">
                Define your infrastructure capacity
              </p>
            </div>
            <button
              class="btn btn-primary gap-2"
              @click="addProviderDialog?.showModal()"
            >
              <svg
                class="size-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add Provider
            </button>
          </div>

          <div class="grid gap-3">
            <div
              v-for="provider in resourceProviders"
              :key="provider.id"
              class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-200 border border-base-300"
            >
              <div class="card-body p-4 flex flex-row items-center gap-4">
                <div class="flex flex-col items-center justify-center w-20 h-20 rounded-lg bg-gradient-to-br from-primary/20 to-primary/5 flex-shrink-0">
                  <svg
                    v-if="provider.type === 'power'"
                    class="w-10 h-10 text-primary"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <svg
                    v-else-if="provider.type === 'cooling'"
                    class="w-10 h-10 text-primary"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <svg
                    v-else-if="provider.type === 'network'"
                    class="w-10 h-10 text-primary"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                  </svg>
                  <span class="text-xs font-semibold mt-1 capitalize">{{ provider.type }}</span>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="card-title text-base mb-2">
                    {{ provider.name }}
                  </h4>
                  <div class="flex flex-wrap gap-2 mb-2">
                    <span
                      v-if="provider.powerCapacity > 0"
                      class="badge badge-primary badge-sm"
                    >{{ provider.powerCapacity }}W</span>
                    <span
                      v-if="provider.powerPortsCapacity > 0"
                      class="badge badge-primary badge-sm"
                    >{{ provider.powerPortsCapacity }} ports</span>
                    <span
                      v-if="provider.coolingCapacity > 0"
                      class="badge badge-accent badge-sm"
                    >{{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
                    <span
                      v-if="provider.networkCapacity > 0"
                      class="badge badge-secondary badge-sm"
                    >{{ provider.networkCapacity }} Gbps</span>
                  </div>
                  <div
                    v-if="provider.location"
                    class="text-xs opacity-70 mb-1"
                  >
                    📍 {{ provider.location }}
                  </div>
                  <p
                    v-if="provider.description"
                    class="text-xs opacity-70 line-clamp-1"
                  >
                    {{ provider.description }}
                  </p>
                </div>
                <div class="card-actions flex-shrink-0 flex flex-col gap-1">
                  <button
                    class="btn btn-ghost btn-xs btn-square hover:btn-primary"
                    title="Edit provider"
                    @click="editProvider(provider)"
                  >
                    <svg
                      class="size-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    class="btn btn-ghost btn-xs btn-square hover:btn-error"
                    title="Delete provider"
                    @click="deleteProvider(provider.id)"
                  >
                    <svg
                      class="size-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <div
              v-if="resourceProviders.length === 0"
              class="text-center py-12 opacity-50"
            >
              <svg
                class="w-16 h-16 mx-auto mb-4 opacity-50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                />
              </svg>
              <p class="text-lg font-semibold mb-2">
                No resource providers yet
              </p>
              <p class="text-sm">
                Add providers to supply power, cooling, and network capacity
              </p>
            </div>
          </div>
        </div>

        <!-- Import/Export Tab -->
        <div
          v-if="activeTab === 'import-export'"
          class="flex-1 overflow-y-auto px-6 pb-6"
        >
          <div class="grid lg:grid-cols-2 gap-6">
            <!-- Export Section -->
            <div class="card bg-gradient-to-br from-success/10 to-success/5 shadow-lg border border-success/20">
              <div class="card-body">
                <h3 class="card-title text-success mb-2">
                  <svg
                    class="size-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  Export Devices
                </h3>
                <p class="text-sm opacity-70 mb-4">
                  Download your custom device groups and devices as a JSON file
                </p>
                <div class="stats shadow mb-4 bg-base-100">
                  <div class="stat py-3 px-4">
                    <div class="stat-title text-xs">
                      Device Groups
                    </div>
                    <div class="stat-value text-2xl text-primary">
                      {{ deviceGroups.length }}
                    </div>
                  </div>
                  <div class="stat py-3 px-4">
                    <div class="stat-title text-xs">
                      Custom Devices
                    </div>
                    <div class="stat-value text-2xl text-secondary">
                      {{ customDevices.length }}
                    </div>
                  </div>
                </div>
                <div class="card-actions justify-end">
                  <button
                    class="btn btn-success gap-2"
                    @click="exportDevices"
                  >
                    <svg
                      class="size-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                      />
                    </svg>
                    Export to JSON
                  </button>
                </div>
              </div>
            </div>

            <!-- Import Section -->
            <div class="card bg-gradient-to-br from-info/10 to-info/5 shadow-lg border border-info/20">
              <div class="card-body">
                <h3 class="card-title text-info mb-2">
                  <svg
                    class="size-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  Import Devices
                </h3>
                <p class="text-sm opacity-70 mb-4">
                  Import device groups and devices from a JSON file
                </p>
                
                <div class="form-control mb-4">
                  <label class="label">
                    <span class="label-text font-semibold">Import Mode</span>
                  </label>
                  <div class="flex gap-2">
                    <label
                      class="btn btn-sm flex-1 cursor-pointer"
                      :class="importMode === 'merge' ? 'btn-primary' : 'btn-outline'"
                    >
                      <input
                        v-model="importMode"
                        type="radio"
                        value="merge"
                        class="hidden"
                      >
                      <svg
                        class="size-4 mr-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                        />
                      </svg>
                      Merge
                    </label>
                    <label
                      class="btn btn-sm flex-1 cursor-pointer"
                      :class="importMode === 'replace' ? 'btn-warning' : 'btn-outline'"
                    >
                      <input
                        v-model="importMode"
                        type="radio"
                        value="replace"
                        class="hidden"
                      >
                      <svg
                        class="size-4 mr-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                        />
                      </svg>
                      Replace
                    </label>
                  </div>
                </div>

                <input
                  ref="fileInput"
                  type="file"
                  accept=".json"
                  class="hidden"
                  @change="handleFileSelect"
                >
                <div class="card-actions justify-end">
                  <button
                    class="btn btn-info gap-2"
                    @click="$refs.fileInput.click()"
                  >
                    <svg
                      class="size-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    Select File
                  </button>
                </div>
                
                <div
                  v-if="importError"
                  class="alert alert-error mt-4 shadow-md"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="stroke-current shrink-0 h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span class="text-sm">{{ importError }}</span>
                </div>
              </div>
            </div>

            <!-- JSON Format Reference -->
            <div class="card bg-base-100 shadow-lg border border-base-300 lg:col-span-2">
              <div class="card-body">
                <h3 class="card-title mb-2">
                  <svg
                    class="size-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                    />
                  </svg>
                  JSON Format Reference
                </h3>
                <p class="text-sm opacity-70 mb-3">
                  Your import file should follow this structure:
                </p>
                <div class="mockup-code text-xs">
                  <pre data-prefix="1"><code>{</code></pre>
                  <pre data-prefix="2"><code>  "groups": [</code></pre>
                  <pre data-prefix="3"><code>    {</code></pre>
                  <pre data-prefix="4"><code>      "id": "group-1",</code></pre>
                  <pre data-prefix="5"><code>      "name": "My Servers",</code></pre>
                  <pre data-prefix="6"><code>      "color": "#9B59B6",</code></pre>
                  <pre data-prefix="7"><code>      "deviceCount": 2</code></pre>
                  <pre data-prefix="8"><code>    }</code></pre>
                  <pre data-prefix="9"><code>  ],</code></pre>
                  <pre data-prefix="10"><code>  "devices": [</code></pre>
                  <pre data-prefix="11"><code>    {</code></pre>
                  <pre data-prefix="12"><code>      "id": "device-1",</code></pre>
                  <pre data-prefix="13"><code>      "name": "Custom Server",</code></pre>
                  <pre data-prefix="14"><code>      "category": "My Servers",</code></pre>
                  <pre data-prefix="15"><code>      "ruSize": 2,</code></pre>
                  <pre data-prefix="16"><code>      "powerDraw": 850,</code></pre>
                  <pre data-prefix="17"><code>      "color": "#9B59B6",</code></pre>
                  <pre data-prefix="18"><code>      "description": "Custom device",</code></pre>
                  <pre data-prefix="19"><code>      "custom": true</code></pre>
                  <pre data-prefix="20"><code>    }</code></pre>
                  <pre data-prefix="21"><code>  ]</code></pre>
                  <pre data-prefix="22"><code>}</code></pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Device Group Dialog -->
  <dialog
    ref="addGroupDialog"
    class="modal"
  >
    <div class="modal-box w-full max-w-md">
      <div class="flex items-center justify-between mb-6 p-6 -mx-6 -mt-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          {{ editingGroup ? 'Edit' : 'Add' }} Device Group
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle text-primary-content opacity-70 hover:opacity-100"
          @click="closeGroupDialog"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div>
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Group Name</span>
          </label>
          <input
            v-model="newGroup.name"
            type="text"
            placeholder="e.g., Servers, Storage, Network"
            class="input input-bordered w-full"
          >
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Default Color</span>
          </label>
          <div class="flex gap-2 items-center">
            <input
              v-model="newGroup.color"
              type="color"
              class="w-16 h-10 rounded cursor-pointer border border-base-300"
            >
            <input
              v-model="newGroup.color"
              type="text"
              placeholder="#4A90E2"
              class="input input-bordered flex-1"
            >
          </div>
        </div>

        <div class="modal-action">
          <button
            class="btn"
            @click="closeGroupDialog"
          >
            Cancel
          </button>
          <button
            :disabled="!newGroup.name?.trim()"
            class="btn btn-primary"
            @click="handleSaveGroup"
          >
            {{ editingGroup ? 'Save Changes' : 'Add Group' }}
          </button>
        </div>
      </div>
    </div>
    <form
      method="dialog"
      class="modal-backdrop"
    >
      <button>close</button>
    </form>
  </dialog>

  <!-- Add Device Dialog -->
  <dialog
    ref="addDeviceDialog"
    class="modal"
  >
    <div class="modal-box w-full max-w-md max-h-[90vh]">
      <div class="flex items-center justify-between mb-6 p-6 -mx-6 -mt-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          {{ editingDevice ? 'Edit' : isDuplicating ? 'Duplicate' : 'Add' }} Device
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle text-primary-content opacity-70 hover:opacity-100"
          @click="closeDeviceDialog"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div style="max-height: 60vh; overflow-y: auto;">
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Device Model Name *</span>
          </label>
          <input
            v-model="newDevice.name"
            type="text"
            placeholder="e.g., Dell PowerEdge R750"
            class="input input-bordered w-full"
            :class="{ 'input-error': validationErrors.name }"
          >
          <label
            v-if="validationErrors.name"
            class="label"
          >
            <span class="label-text-alt text-error">{{ validationErrors.name }}</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Device Group *</span>
          </label>
          <select
            v-model="newDevice.category"
            class="select select-bordered w-full"
            :class="{ 'select-error': validationErrors.category }"
          >
            <option value="">
              Select a group...
            </option>
            <option
              v-for="group in deviceGroups"
              :key="group.id"
              :value="group.name"
            >
              {{ group.name }}
            </option>
          </select>
          <label class="label">
            <span
              v-if="validationErrors.category"
              class="label-text-alt text-error"
            >{{ validationErrors.category }}</span>
            <span
              v-else
              class="label-text-alt"
            >Create new groups in the "Device Groups" tab</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">RU Size (Rack Units) *</span>
          </label>
          <input
            v-model.number="newDevice.ruSize"
            type="number"
            min="1"
            max="42"
            placeholder="e.g., 2"
            class="input input-bordered w-full"
            :class="{ 'input-error': validationErrors.ruSize }"
          >
          <label class="label">
            <span
              v-if="validationErrors.ruSize"
              class="label-text-alt text-error"
            >{{ validationErrors.ruSize }}</span>
            <span
              v-else
              class="label-text-alt"
            >1U = 1.75 inches (44.45mm)</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Power Draw (Watts) *</span>
          </label>
          <input
            v-model.number="newDevice.powerDraw"
            type="number"
            min="0"
            placeholder="e.g., 750"
            class="input input-bordered w-full"
            :class="{ 'input-error': validationErrors.powerDraw }"
          >
          <label class="label">
            <span
              v-if="validationErrors.powerDraw"
              class="label-text-alt text-error"
            >{{ validationErrors.powerDraw }}</span>
            <span
              v-else
              class="label-text-alt"
            >Maximum power consumption under load</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Power Ports Used *</span>
          </label>
          <input
            v-model.number="newDevice.powerPortsUsed"
            type="number"
            min="0"
            placeholder="e.g., 2 for dual PSU"
            class="input input-bordered w-full"
            :class="{ 'input-error': validationErrors.powerPortsUsed }"
          >
          <label class="label">
            <span
              v-if="validationErrors.powerPortsUsed"
              class="label-text-alt text-error"
            >{{ validationErrors.powerPortsUsed }}</span>
            <span
              v-else
              class="label-text-alt"
            >Number of PDU power ports required (1 for single PSU, 2 for dual PSU, etc.)</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Color</span>
          </label>
          <div class="flex gap-2 items-center">
            <input
              v-model="newDevice.color"
              type="color"
              class="w-16 h-10 rounded cursor-pointer border border-base-300"
            >
            <input
              v-model="newDevice.color"
              type="text"
              placeholder="#4A90E2"
              class="input input-bordered flex-1"
            >
          </div>
          <label class="label">
            <span class="label-text-alt">Uses group default color if not specified</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Description (Optional)</span>
          </label>
          <textarea
            v-model="newDevice.description"
            rows="3"
            placeholder="Additional details about this device..."
            class="textarea textarea-bordered w-full"
          />
        </div>

        <div class="modal-action">
          <button
            class="btn"
            @click="closeDeviceDialog"
          >
            Cancel
          </button>
          <button
            :disabled="!canAddDevice"
            class="btn btn-primary"
            @click="handleSaveDevice"
          >
            {{ editingDevice ? 'Save Changes' : isDuplicating ? 'Create Duplicate' : 'Add Device' }}
          </button>
        </div>
      </div>
    </div>
    <form
      method="dialog"
      class="modal-backdrop"
    >
      <button>close</button>
    </form>
  </dialog>

  <!-- Add/Edit Resource Provider Dialog -->
  <dialog
    ref="addProviderDialog"
    class="modal"
  >
    <div class="modal-box w-full max-w-md max-h-[90vh]">
      <div class="flex items-center justify-between mb-6 p-6 -mx-6 -mt-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          {{ editingProvider ? 'Edit' : 'Add' }} Resource Provider
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle text-primary-content opacity-70 hover:opacity-100"
          @click="closeProviderDialog"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div style="max-height: 60vh; overflow-y: auto;">
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Provider Name *</span>
          </label>
          <input
            v-model="newProvider.name"
            type="text"
            placeholder="e.g., PDU-A01, CRAC-02, Network Switch"
            class="input input-bordered w-full"
          >
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Provider Type *</span>
          </label>
          <select
            v-model="newProvider.type"
            class="select select-bordered w-full"
          >
            <option value="">
              Select type...
            </option>
            <option value="power">
              Power (PDU, UPS, Generator)
            </option>
            <option value="cooling">
              Cooling (HVAC, CRAC, CRAH)
            </option>
          </select>
          <label class="label">
            <span class="label-text-alt">What type of resource does this provide?</span>
          </label>
        </div>

        <!-- Power Capacity (shown for power type) -->
        <div
          v-if="newProvider.type === 'power'"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Power Capacity (Watts) *</span>
          </label>
          <input
            v-model.number="newProvider.powerCapacity"
            type="number"
            min="0"
            placeholder="e.g., 20000"
            class="input input-bordered w-full"
          >
          <label class="label">
            <span class="label-text-alt">Maximum power this provider can supply</span>
          </label>
        </div>

        <!-- Power Ports Capacity (shown for power type) -->
        <div
          v-if="newProvider.type === 'power'"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Power Ports Capacity *</span>
          </label>
          <input
            v-model.number="newProvider.powerPortsCapacity"
            type="number"
            min="0"
            placeholder="e.g., 24"
            class="input input-bordered w-full"
          >
          <label class="label">
            <span class="label-text-alt">Number of available power ports on this PDU</span>
          </label>
        </div>

        <!-- Cooling Capacity (shown for cooling type) -->
        <div
          v-if="newProvider.type === 'cooling'"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Cooling Capacity (Refrigeration Tons) *</span>
          </label>
          <input
            v-model.number="newProvider.coolingCapacityTons"
            type="number"
            min="0"
            step="0.1"
            placeholder="e.g., 5"
            class="input input-bordered w-full"
          >
          <label class="label">
            <span class="label-text-alt">1 Refrigeration Ton = 12,000 BTU/hr</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Location (Optional)</span>
          </label>
          <input
            v-model="newProvider.location"
            type="text"
            placeholder="e.g., Row A, Room 101, Cabinet 5"
            class="input input-bordered w-full"
          >
        </div>

        <!-- RU Size (optional - 0 means not racked) -->
        <div class="mb-4">
          <label class="label">
            <span class="label-text">RU Size (Rack Units)</span>
          </label>
          <input
            v-model.number="newProvider.ruSize"
            type="number"
            min="0"
            max="42"
            placeholder="0"
            class="input input-bordered w-full"
          >
          <label class="label">
            <span class="label-text-alt">Set to 1 or more to allow dragging into racks. 0 means not rackable.</span>
          </label>
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Description (Optional)</span>
          </label>
          <textarea
            v-model="newProvider.description"
            rows="3"
            placeholder="Additional details about this provider..."
            class="textarea textarea-bordered w-full"
          />
        </div>

        <div class="modal-action">
          <button
            class="btn"
            @click="closeProviderDialog"
          >
            Cancel
          </button>
          <button
            :disabled="!canAddProvider"
            class="btn btn-primary"
            @click="handleSaveProvider"
          >
            {{ editingProvider ? 'Save Changes' : 'Add Provider' }}
          </button>
        </div>
      </div>
    </div>
    <form
      method="dialog"
      class="modal-backdrop"
    >
      <button>close</button>
    </form>
  </dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useToast } from '../composables/useToast';
import { useResourceProviders } from '../composables/useResourceProviders';
import { logError, logWarn, logInfo, logDebug } from '../utils/logger';

const props = defineProps({
  initialTab: {
    type: String,
    default: 'groups'
  }
})

const { showToast } = useToast();
const { 
  resourceProviders,
  addProvider: addResourceProvider,
  updateProvider: updateResourceProvider,
  deleteProvider: deleteResourceProvider
} = useResourceProviders();

const activeTab = ref(props.initialTab);

// Watch for changes to initialTab prop
watch(() => props.initialTab, (newTab) => {
  activeTab.value = newTab
})

const addGroupDialog = ref(null);
const addDeviceDialog = ref(null);
const addProviderDialog = ref(null);
const editingGroup = ref(null);
const editingDevice = ref(null);
const editingProvider = ref(null);
const isDuplicating = ref(false);

const deviceGroups = ref([]);
const customDevices = ref([]);

const newGroup = ref({
  name: '',
  color: '#4A90E2'
});

const newDevice = ref({
  name: '',
  category: '',
  ruSize: 1,
  powerDraw: 0,
  powerPortsUsed: 1,
  color: '',
  description: ''
});

const validationErrors = ref({
  name: '',
  category: '',
  ruSize: '',
  powerDraw: ''
});

const newProvider = ref({
  name: '',
  type: '',
  powerCapacity: 0,
  powerPortsCapacity: 0,
  coolingCapacityTons: 0,
  location: '',
  description: '',
  ruSize: 0
});

const importMode = ref('merge');
const importError = ref('');
const fileInput = ref(null);

const canAddDevice = computed(() => {
  return newDevice.value.name?.trim() &&
         newDevice.value.category &&
         newDevice.value.ruSize > 0 &&
         newDevice.value.powerDraw >= 0 &&
         newDevice.value.powerPortsUsed >= 0;
});

const canAddProvider = computed(() => {
  if (!newProvider.value.name?.trim() || !newProvider.value.type) {
    return false;
  }
  
  // Check that at least one capacity is provided for the selected type
  if (newProvider.value.type === 'power') {
    return newProvider.value.powerCapacity > 0;
  } else if (newProvider.value.type === 'cooling') {
    return newProvider.value.coolingCapacityTons > 0;
  } else if (newProvider.value.type === 'network') {
    return newProvider.value.networkCapacity > 0;
  }
  
  return false;
});

onMounted(() => {
  loadDeviceGroups();
  loadCustomDevices();
});

async function loadDeviceGroups() {
  // Load groups from both API (database) and localStorage, then merge them
  const localGroups = [];
  const apiGroups = [];

  // Load from localStorage
  const saved = localStorage.getItem('racker-device-groups');
  if (saved) {
    try {
      localGroups.push(...JSON.parse(saved));
    } catch (err) {
      logError('Error loading device groups from localStorage', err);
    }
  }

  // Load from API (database)
  try {
    const response = await fetch('/api/device-groups');
    if (response.ok) {
      const groups = await response.json();
      apiGroups.push(...groups);
    }
  } catch (err) {
    logWarn('Could not load device groups from API', err);
  }

  // Merge groups: combine both sources, avoiding duplicates by name
  const mergedGroups = [];
  const seenNames = new Set();

  // Add API groups first (they have priority)
  for (const group of apiGroups) {
    const normalizedName = group.name.toLowerCase();
    if (!seenNames.has(normalizedName)) {
      seenNames.add(normalizedName);
      // Convert API format to local format
      mergedGroups.push({
        id: `api-${group.id}`,
        name: group.name,
        color: '#4A90E2', // Default color for API groups
        deviceCount: group.device_count || 0
      });
    }
  }

  // Add localStorage groups that don't conflict
  for (const group of localGroups) {
    const normalizedName = group.name.toLowerCase();
    if (!seenNames.has(normalizedName)) {
      seenNames.add(normalizedName);
      mergedGroups.push(group);
    }
  }

  deviceGroups.value = mergedGroups;
}

function loadCustomDevices() {
  const saved = localStorage.getItem('racker-custom-devices');
  if (saved) {
    try {
      customDevices.value = JSON.parse(saved);
    } catch (err) {
      logError('Error loading custom devices', err);
    }
  }
}

function saveDeviceGroups() {
  localStorage.setItem('racker-device-groups', JSON.stringify(deviceGroups.value));
}

function saveCustomDevices() {
  localStorage.setItem('racker-custom-devices', JSON.stringify(customDevices.value));
}

function validateDevice() {
  validationErrors.value = {
    name: '',
    category: '',
    ruSize: '',
    powerDraw: ''
  };

  let isValid = true;

  if (!newDevice.value.name?.trim()) {
    validationErrors.value.name = 'Device name is required';
    isValid = false;
  } else if (newDevice.value.name.length < 3) {
    validationErrors.value.name = 'Device name must be at least 3 characters';
    isValid = false;
  }

  if (!newDevice.value.category) {
    validationErrors.value.category = 'Please select a device group';
    isValid = false;
  }

  if (!newDevice.value.ruSize || newDevice.value.ruSize < 1 || newDevice.value.ruSize > 42) {
    validationErrors.value.ruSize = 'RU size must be between 1 and 42';
    isValid = false;
  }

  if (newDevice.value.powerDraw === null || newDevice.value.powerDraw === undefined || newDevice.value.powerDraw < 0) {
    validationErrors.value.powerDraw = 'Power draw must be 0 or greater';
    isValid = false;
  }

  return isValid;
}

function closeGroupDialog() {
  addGroupDialog.value?.close();
  editingGroup.value = null;
  newGroup.value = {
    name: '',
    color: '#4A90E2'
  };
}

function closeDeviceDialog() {
  addDeviceDialog.value?.close();
  editingDevice.value = null;
  isDuplicating.value = false;
  newDevice.value = {
    name: '',
    category: '',
    ruSize: 1,
    powerDraw: 0,
    powerPortsUsed: 1,
    color: '',
    description: ''
  };
  validationErrors.value = {
    name: '',
    category: '',
    ruSize: '',
    powerDraw: ''
  };
}

function editGroup(group) {
  editingGroup.value = group;
  newGroup.value = {
    name: group.name,
    color: group.color
  };
  addGroupDialog.value?.showModal();
}

function handleSaveGroup() {
  if (!newGroup.value.name?.trim()) return;

  if (editingGroup.value) {
    // Update existing group
    const index = deviceGroups.value.findIndex(g => g.id === editingGroup.value.id);
    if (index !== -1) {
      deviceGroups.value[index] = {
        ...deviceGroups.value[index],
        name: newGroup.value.name.trim(),
        color: newGroup.value.color
      };
      
      // Update category name in devices if group name changed
      if (editingGroup.value.name !== newGroup.value.name.trim()) {
        customDevices.value.forEach(device => {
          if (device.category === editingGroup.value.name) {
            device.category = newGroup.value.name.trim();
          }
        });
        saveCustomDevices();
      }
      
      showToast('success', 'Device group updated');
    }
  } else {
    // Add new group
    const group = {
      id: `group-${Date.now()}`,
      name: newGroup.value.name.trim(),
      color: newGroup.value.color,
      deviceCount: 0
    };
    deviceGroups.value.push(group);
    showToast('success', 'Device group added');
  }

  saveDeviceGroups();
  closeGroupDialog();
  
  // Notify other components
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function deleteGroup(groupId) {
  const group = deviceGroups.value.find(g => g.id === groupId);
  if (!confirm(`Delete device group "${group.name}"? Devices in this group will not be deleted.`)) {
    return;
  }

  deviceGroups.value = deviceGroups.value.filter(g => g.id !== groupId);
  saveDeviceGroups();
  showToast('success', 'Device group deleted');
  
  // Notify other components
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function editDevice(device) {
  editingDevice.value = device;
  isDuplicating.value = false;
  newDevice.value = {
    name: device.name,
    category: device.category,
    ruSize: device.ruSize,
    powerDraw: device.powerDraw,
    powerPortsUsed: device.powerPortsUsed || 1,
    color: device.color,
    description: device.description || ''
  };
  addDeviceDialog.value?.showModal();
}

function duplicateDevice(device) {
  editingDevice.value = null;
  isDuplicating.value = true;
  newDevice.value = {
    name: `${device.name} (Copy)`,
    category: device.category,
    ruSize: device.ruSize,
    powerDraw: device.powerDraw,
    powerPortsUsed: device.powerPortsUsed || 1,
    color: device.color,
    description: device.description || ''
  };
  addDeviceDialog.value?.showModal();
}

function handleSaveDevice() {
  if (!validateDevice()) return;

  // Get color from group if not specified
  let color = newDevice.value.color;
  if (!color) {
    const group = deviceGroups.value.find(g => g.name === newDevice.value.category);
    color = group?.color || '#4A90E2';
  }

  if (editingDevice.value && !isDuplicating.value) {
    // Update existing device
    const index = customDevices.value.findIndex(d => d.id === editingDevice.value.id);
    if (index !== -1) {
      customDevices.value[index] = {
        ...customDevices.value[index],
        name: newDevice.value.name.trim(),
        category: newDevice.value.category,
        ruSize: newDevice.value.ruSize,
        powerDraw: newDevice.value.powerDraw,
        color: color,
        description: newDevice.value.description?.trim() || ''
      };
      showToast('success', 'Device updated');
    }
  } else {
    // Add new device (or duplicate)
    const device = {
      id: `device-${Date.now()}`,
      name: newDevice.value.name.trim(),
      category: newDevice.value.category,
      ruSize: newDevice.value.ruSize,
      powerDraw: newDevice.value.powerDraw,
      color: color,
      description: newDevice.value.description?.trim() || '',
      custom: true
    };
    customDevices.value.push(device);
    showToast('success', isDuplicating.value ? 'Device duplicated' : 'Device added');
  }

  saveCustomDevices();
  updateGroupCounts();
  closeDeviceDialog();
  
  // Emit event to notify parent to reload devices
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function deleteDevice(deviceId) {
  const device = customDevices.value.find(d => d.id === deviceId);
  if (!confirm(`Delete device "${device.name}"?`)) {
    return;
  }

  customDevices.value = customDevices.value.filter(d => d.id !== deviceId);
  saveCustomDevices();
  updateGroupCounts();
  showToast('success', 'Device deleted');

  // Emit event to notify parent to reload devices
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function updateGroupCounts() {
  deviceGroups.value.forEach(group => {
    group.deviceCount = customDevices.value.filter(d => d.category === group.name).length;
  });
  saveDeviceGroups();
}

function closeProviderDialog() {
  addProviderDialog.value?.close();
  editingProvider.value = null;
  newProvider.value = {
    name: '',
    type: '',
    powerCapacity: 0,
    powerPortsCapacity: 0,
    coolingCapacityTons: 0,
    networkCapacity: 0,
    location: '',
    description: '',
    ruSize: 0
  };
}

function editProvider(provider) {
  editingProvider.value = provider;
  newProvider.value = {
    name: provider.name,
    type: provider.type,
    powerCapacity: provider.powerCapacity || 0,
    powerPortsCapacity: provider.powerPortsCapacity || 0,
    coolingCapacityTons: provider.coolingCapacity ? provider.coolingCapacity / 12000 : 0,
    networkCapacity: provider.networkCapacity || 0,
    location: provider.location || '',
    description: provider.description || '',
    ruSize: provider.ruSize || 0
  };
  addProviderDialog.value?.showModal();
}

function handleSaveProvider() {
  if (!canAddProvider.value) return;

  const providerData = {
    name: newProvider.value.name.trim(),
    type: newProvider.value.type,
    powerCapacity: newProvider.value.type === 'power' ? newProvider.value.powerCapacity : 0,
    powerPortsCapacity: newProvider.value.type === 'power' ? newProvider.value.powerPortsCapacity : 0,
    coolingCapacity: newProvider.value.type === 'cooling' ? newProvider.value.coolingCapacityTons * 12000 : 0,
    networkCapacity: newProvider.value.type === 'network' ? newProvider.value.networkCapacity : 0,
    location: newProvider.value.location?.trim() || '',
    description: newProvider.value.description?.trim() || '',
    ruSize: newProvider.value.ruSize || 0
  };

  if (editingProvider.value) {
    // Update existing provider
    updateResourceProvider(editingProvider.value.id, providerData);
    showToast('success', 'Resource provider updated');
  } else {
    // Add new provider
    addResourceProvider(providerData);
    showToast('success', 'Resource provider added');
  }

  closeProviderDialog();
}

function deleteProvider(providerId) {
  const provider = resourceProviders.value.find(p => p.id === providerId);
  if (!confirm(`Delete resource provider "${provider.name}"?`)) {
    return;
  }

  deleteResourceProvider(providerId);
  showToast('success', 'Resource provider deleted');
}

function exportDevices() {
  const exportData = {
    groups: deviceGroups.value,
    devices: customDevices.value,
    exportDate: new Date().toISOString(),
    version: '1.0'
  };

  const dataStr = JSON.stringify(exportData, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `racker-devices-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  
  showToast('success', 'Devices exported successfully');
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  importError.value = '';
  
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      importDevices(data);
    } catch (err) {
      importError.value = 'Invalid JSON file. Please check the file format.';
      logError('Import error', err);
    }
  };
  
  reader.onerror = () => {
    importError.value = 'Error reading file. Please try again.';
  };
  
  reader.readAsText(file);
  
  // Reset file input
  event.target.value = '';
}

function importDevices(data) {
  try {
    // Validate data structure
    if (!data.groups || !Array.isArray(data.groups)) {
      throw new Error('Invalid data: missing or invalid "groups" array');
    }
    if (!data.devices || !Array.isArray(data.devices)) {
      throw new Error('Invalid data: missing or invalid "devices" array');
    }
    
    // Validate required fields
    for (const group of data.groups) {
      if (!group.name || !group.color) {
        throw new Error('Invalid group: missing required fields (name, color)');
      }
    }
    
    for (const device of data.devices) {
      if (!device.name || !device.category || device.ruSize === undefined || device.powerDraw === undefined) {
        throw new Error('Invalid device: missing required fields (name, category, ruSize, powerDraw)');
      }
    }
    
    if (importMode.value === 'replace') {
      // Replace mode: clear existing data
      if (!confirm('This will replace all your existing custom devices and groups. Continue?')) {
        return;
      }
      deviceGroups.value = data.groups;
      customDevices.value = data.devices;
    } else {
      // Merge mode: combine with existing data
      const existingGroupIds = new Set(deviceGroups.value.map(g => g.id));
      const existingDeviceIds = new Set(customDevices.value.map(d => d.id));
      
      let groupsAdded = 0;
      let devicesAdded = 0;
      
      // Add new groups
      for (const group of data.groups) {
        if (!existingGroupIds.has(group.id)) {
          deviceGroups.value.push(group);
          groupsAdded++;
        }
      }
      
      // Add new devices
      for (const device of data.devices) {
        if (!existingDeviceIds.has(device.id)) {
          customDevices.value.push(device);
          devicesAdded++;
        }
      }
      
      showToast('success', `Imported ${groupsAdded} groups and ${devicesAdded} devices`);
    }
    
    saveDeviceGroups();
    saveCustomDevices();
    updateGroupCounts();
    
    if (importMode.value === 'replace') {
      showToast('success', 'Devices replaced successfully');
    }
    
    // Notify other components
    window.dispatchEvent(new CustomEvent('devices-updated'));
  } catch (err) {
    importError.value = err.message;
    logError('Import error', err);
  }
}
</script>
