declare module 'astro:content' {
	interface RenderResult {
		Content: import('astro/runtime/server/index.js').AstroComponentFactory;
		headings: import('astro').MarkdownHeading[];
		remarkPluginFrontmatter: Record<string, any>;
	}
	interface Render {
		'.md': Promise<RenderResult>;
	}

	export interface RenderedContent {
		html: string;
		metadata?: {
			imagePaths: Array<string>;
			[key: string]: unknown;
		};
	}
}

declare module 'astro:content' {
	type Flatten<T> = T extends { [K: string]: infer U } ? U : never;

	export type CollectionKey = keyof AnyEntryMap;
	export type CollectionEntry<C extends CollectionKey> = Flatten<AnyEntryMap[C]>;

	export type ContentCollectionKey = keyof ContentEntryMap;
	export type DataCollectionKey = keyof DataEntryMap;

	type AllValuesOf<T> = T extends any ? T[keyof T] : never;
	type ValidContentEntrySlug<C extends keyof ContentEntryMap> = AllValuesOf<
		ContentEntryMap[C]
	>['slug'];

	/** @deprecated Use `getEntry` instead. */
	export function getEntryBySlug<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		// Note that this has to accept a regular string too, for SSR
		entrySlug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;

	/** @deprecated Use `getEntry` instead. */
	export function getDataEntryById<C extends keyof DataEntryMap, E extends keyof DataEntryMap[C]>(
		collection: C,
		entryId: E,
	): Promise<CollectionEntry<C>>;

	export function getCollection<C extends keyof AnyEntryMap, E extends CollectionEntry<C>>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => entry is E,
	): Promise<E[]>;
	export function getCollection<C extends keyof AnyEntryMap>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => unknown,
	): Promise<CollectionEntry<C>[]>;

	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(entry: {
		collection: C;
		slug: E;
	}): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(entry: {
		collection: C;
		id: E;
	}): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		slug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(
		collection: C,
		id: E,
	): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;

	/** Resolve an array of entry references from the same collection */
	export function getEntries<C extends keyof ContentEntryMap>(
		entries: {
			collection: C;
			slug: ValidContentEntrySlug<C>;
		}[],
	): Promise<CollectionEntry<C>[]>;
	export function getEntries<C extends keyof DataEntryMap>(
		entries: {
			collection: C;
			id: keyof DataEntryMap[C];
		}[],
	): Promise<CollectionEntry<C>[]>;

	export function render<C extends keyof AnyEntryMap>(
		entry: AnyEntryMap[C][string],
	): Promise<RenderResult>;

	export function reference<C extends keyof AnyEntryMap>(
		collection: C,
	): import('astro/zod').ZodEffects<
		import('astro/zod').ZodString,
		C extends keyof ContentEntryMap
			? {
					collection: C;
					slug: ValidContentEntrySlug<C>;
				}
			: {
					collection: C;
					id: keyof DataEntryMap[C];
				}
	>;
	// Allow generic `string` to avoid excessive type errors in the config
	// if `dev` is not running to update as you edit.
	// Invalid collection names will be caught at build time.
	export function reference<C extends string>(
		collection: C,
	): import('astro/zod').ZodEffects<import('astro/zod').ZodString, never>;

	type ReturnTypeOrOriginal<T> = T extends (...args: any[]) => infer R ? R : T;
	type InferEntrySchema<C extends keyof AnyEntryMap> = import('astro/zod').infer<
		ReturnTypeOrOriginal<Required<ContentConfig['collections'][C]>['schema']>
	>;

	type ContentEntryMap = {
		"posts": {
"00-每日文章汇总-2026-08-09.md": {
	id: "00-每日文章汇总-2026-08-09.md";
  slug: "00-每日文章汇总-2026-08-09";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"01-大语言模型作为健康信息工具患者在耳鼻喉科的使用与信任研究.md": {
	id: "01-大语言模型作为健康信息工具患者在耳鼻喉科的使用与信任研究.md";
  slug: "01-大语言模型作为健康信息工具患者在耳鼻喉科的使用与信任研究";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"02-ai在感染性疾病决策中的应用从床旁咨询到复杂护理.md": {
	id: "02-ai在感染性疾病决策中的应用从床旁咨询到复杂护理.md";
  slug: "02-ai在感染性疾病决策中的应用从床旁咨询到复杂护理";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"03-rsna肺栓塞检测挑战赛top2模型外部验证泛化能力评估.md": {
	id: "03-rsna肺栓塞检测挑战赛top2模型外部验证泛化能力评估.md";
  slug: "03-rsna肺栓塞检测挑战赛top2模型外部验证泛化能力评估";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"04-ai在肾肿块检测特征表征与管理中的应用叙事性综述.md": {
	id: "04-ai在肾肿块检测特征表征与管理中的应用叙事性综述.md";
  slug: "04-ai在肾肿块检测特征表征与管理中的应用叙事性综述";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"05-数字病理ai助力mash纤维化定量评估需求进展与挑战.md": {
	id: "05-数字病理ai助力mash纤维化定量评估需求进展与挑战.md";
  slug: "05-数字病理ai助力mash纤维化定量评估需求进展与挑战";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"06-医疗ai-2026从技术突破走向临床落地.md": {
	id: "06-医疗ai-2026从技术突破走向临床落地.md";
  slug: "06-医疗ai-2026从技术突破走向临床落地";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
};

	};

	type DataEntryMap = {
		
	};

	type AnyEntryMap = ContentEntryMap & DataEntryMap;

	export type ContentConfig = never;
}
