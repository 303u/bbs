<template>
  <n-config-provider :theme="$store.getters.theme" :locale="$store.getters.locale"
    :date-locale="$store.getters.locale_d">
    <n-dialog-provider>
      <n-message-provider>
        <n-loading-bar-provider>
          <router-view></router-view>
        </n-loading-bar-provider>
      </n-message-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>
