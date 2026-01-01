<script setup lang="ts">
import type { WelcomeMessage } from '@/types/dynamic-messages';
import DOMPurify from 'dompurify';
import { checkIfDevelopment } from '@shared/utils';
import { ofetch } from 'ofetch';
import ExternalLink from '@/components/helper/ExternalLink.vue';
import FadeTransition from '@/components/helper/FadeTransition.vue';
import { useRandomStepper } from '@/composables/random-stepper';
import { logger } from '@/utils/logging';

const props = defineProps<{
  messages: WelcomeMessage[];
}>();

const svg = ref<string>();

const { onNavigate, onPause, onResume, step, steps } = useRandomStepper(props.messages.length);

const activeItem = computed<WelcomeMessage>(() => props.messages[get(step) - 1]);

/**
 * Sanitizes SVG content to prevent XSS attacks.
 * Removes all script elements, event handlers, and potentially dangerous attributes.
 */
function sanitizeSvg(svgContent: string): string {
  return DOMPurify.sanitize(svgContent, {
    USE_PROFILES: { svg: true, svgFilters: true },
    ADD_TAGS: ['use'],
    FORBID_TAGS: ['script', 'style'],
    FORBID_ATTR: ['onload', 'onerror', 'onclick', 'onmouseover', 'onfocus', 'onblur'],
  });
}

async function fetchSvg(): Promise<string | null> {
  const url = get(activeItem).icon;

  if (!url || !(checkIfDevelopment() || url.startsWith(`https://raw.githubusercontent.com/rotki/data`)))
    return null;

  try {
    const rawSvg = await ofetch(url, { responseType: 'text' });
    return sanitizeSvg(rawSvg);
  }
  catch (error: any) {
    logger.error(error);
    return null;
  }
}

watch(activeItem, async (value, oldValue) => {
  if (value.icon && oldValue.icon !== value.icon)
    set(svg, await fetchSvg());
});

onMounted(async () => {
  if (get(activeItem)?.icon)
    set(svg, await fetchSvg());
});
</script>

<template>
  <div
    v-if="activeItem"
    class="flex flex-col items-start gap-4 w-full p-6 overflow-hidden rounded-lg bg-[rgba(78,91,166,0.04)]"
  >
    <FadeTransition tag="div">
      <div
        :key="step"
        class="flex flex-col items-start gap-4"
        @mouseover="onPause()"
        @mouseleave="onResume()"
      >
        <div
          v-if="activeItem.icon"
          class="bg-white rounded-[0.625rem] p-3"
        >
          <div
            class="object-contain text-rui-primary h-6 w-6 [&_svg_path]:!fill-rui-primary"
            v-html="svg"
          />
        </div>
        <div
          v-if="activeItem.header"
          class="text-h6 text-rui-text"
        >
          {{ activeItem.header }}
        </div>
        <div class="text-body-1 text-rui-text-secondary whitespace-break-spaces">
          {{ activeItem.text }}
        </div>
      </div>
    </FadeTransition>

    <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-x-3 gap-y-6 w-full">
      <ExternalLink
        v-if="activeItem.action"
        :url="activeItem.action.url || ''"
        custom
        @mouseover="onPause()"
        @mouseleave="onResume()"
      >
        <RuiButton color="primary">
          {{ activeItem.action.text }}
        </RuiButton>
      </ExternalLink>

      <RuiFooterStepper
        v-if="steps > 1"
        :model-value="step"
        :pages="steps"
        variant="bullet"
        hide-buttons
        @update:model-value="onNavigate($event)"
      />
    </div>
  </div>
</template>
