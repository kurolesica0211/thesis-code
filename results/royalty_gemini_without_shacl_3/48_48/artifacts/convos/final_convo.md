================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Wilhelmina (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch pronunciation:  i; Wilhelmina Helena Pauline Maria; 31 August 1880 – 28 November 1962) was Queen of the Netherlands from 1890 until her abdication in 1948.
The only surviving child of King William III of the Netherlands and Emma of Waldeck and Pyrmont, Wilhelmina ascended the throne at the age of 10 after her father's death in 1890, under her mother's regency.
After taking charge of government, Wilhelmina became generally popular for maintaining Dutch neutrality during the First World War and solving many of her country's industrial problems.
Following the German invasion of the Netherlands in 1940, Wilhelmina fled to Britain and took charge of the Dutch government-in-exile.
By 1948, she had returned to the liberated Netherlands and was the only survivor of the 17 European monarchs who were reigning at the time of her inauguration.
Increasingly beset by poor health, Wilhelmina abdicated in favour of her daughter Juliana in September 1948 and retired to Het Loo Palace, where she died in 1962.
Largely due to her status as a symbol of the Resistance, she remains reasonably popular in the Netherlands, even among the Dutch Republican movement.
Youth

Wilhelmina Helena Pauline Maria of Orange-Nassau was born on 31 August 1880, in Noordeinde Palace, The Hague, Netherlands.
She was the only child of King William III and Queen Emma.
In her memoir, Lonely But Not Alone, Wilhelmina wrote that she recalled her father riding horses.
Under the Semi-Salic system of inheritance that was in place in the Netherlands until 1887, Wilhelmina was third in line to the throne from birth.
Her father had had three sons with his first wife, Sophie of Württemberg, but two of them had died before Wilhelmina's birth.
The only other surviving male relatives from the House of Orange were Wilhelmina's great-uncle Frederick, who died in 1881 when Wilhelmina was one year old, and her half-brother Alexander, who died before she turned four.
King William III died on 23 November 1890 and 10-year-old Wilhelmina became Queen of the Netherlands, though her mother was named regent.
In 1895, Wilhelmina visited Queen Victoria of the United Kingdom, who penned an evaluation in her diary: "The young Queen ... still has her hair hanging loose.
"


Wilhelmina turned 18 on 31 August 1898, and was thus entitled to exercise the royal prerogative in her own right.
Reflecting popular opinion in the Netherlands at the time, Wilhelmina expressed a level of disdain towards the British for their annexations of the Transvaal Republic and the Orange Free State in the Boer War.
The Boers were descended from Dutch colonists who migrated to the region while it was a Dutch colony, and the Dutch people, Wilhelmina included, felt a close level of affinity towards them.
In one conversation with her former governess, the Briton Elisabeth Saxton Winter, Wilhelmina referred to the Boer commandos as "excellent shots".
During the war, Wilhelmina ordered the Dutch cruiser HNLMS Gelderland to Portuguese East Africa to evacuate Paul Kruger, the president of the South African Republic.
Marriage

On 7 February 1901 in The Hague, Queen Wilhelmina married Duke Henry of Mecklenburg-Schwerin.
Prince Henry was known to have had numerous extra-marital affairs, at least one of which resulted in illegitimate offspring.
On 9 November, nine months after her marriage, Wilhelmina suffered a miscarriage.
During this time Wilhelmina's heir presumptive was her first cousin once removed William Ernest, Grand Duke of Saxe-Weimar-Eisenach.
As it was assumed that the former would renounce his claim to the Dutch throne and that the latter was too elderly at 57 to become queen, Marie Alexandrine's eldest son, German Prince Heinrich XXXII Reuss of Köstritz, stood in line to succeed Wilhelmina if she had no surviving children.
The birth of Princess Juliana, on 30 April 1909, was met with great relief after eight years of her childless marriage.
Wilhelmina, who formed a close relationship with her daughter, suffered two further miscarriages on 23 January and 20 October 1912.
Wilhelmina and Juliana would be the last Dutch royal babies to survive childbirth until Juliana's daughter Beatrix was born in 1938.
I

Before the First World War began, Wilhelmina visited the powerful German Emperor Wilhelm II.
Partly due to her political influence, the Netherlands remained neutral during World War I.
However, the Allies included the Netherlands in their blockade of Germany, intercepting all Dutch ships and severely restricting Dutch imports to ensure that goods could not be passed on to Germany.
Being a woman, Wilhelmina could not be the supreme commander , but still used every opportunity she had to inspect the Crown forces.
On 6 September 1916 Wilhelmina was aboard the Dutch submarine O 3 while it performed underwater exercises.
This made Wilhemina the second head of state, after the American president Theodore Roosevelt who was the first, to sail and dive aboard a submarine.
In June 1917, Wilhelmina returned from a two-day visit to Zaltbommel on the train that derailed at Houten, but remained unharmed and helped to take care of the injured.
Civil unrest gripped the Netherlands after the war, spurred by the end of the Russian Empire.
However, Wilhelmina's popularity helped restore confidence in the government.
At the end of World War I, Kaiser Wilhelm fled to the Netherlands, where he was granted political asylum, partly owing to his familial links with the royal family.
In response to Allied efforts to get their hands on the deposed Kaiser, Wilhelmina called the Allies' ambassadors to her presence and lectured them on the rights of asylum.
Interwar period

Wilhelmina had a keen understanding of business matters.
During the 1920s and 1930s, the Netherlands began to emerge as an industrial power with the help of the Queen's funds.
Engineers reclaimed vast amounts of land that had been under water by building the Zuiderzee Works, the largest hydraulic engineering project undertaken by the Netherlands during the 20th century.
However, Wilhelmina intervened because she felt the planned location was "too close" to the royal family's summer residence.
Aside from economical and security matters, Queen Wilhelmina used most of the 1930s to find a suitable husband for Juliana.
Many prospects from the United Kingdom and Sweden either declined or were turned down by Juliana.
Finally, mother and daughter found a suitable match in German Prince Bernhard of Lippe-Biesterfeld.
Wilhelmina had her lawyers draft a very detailed prenuptial agreement that specified exactly what her future son-in-law could and could not do.
World War II

On 10 May 1940, Germany invaded the Netherlands.
Despite her hostility towards the British, the almost sixty-year-old Queen Wilhelmina and her family fled The Hague and boarded HMS Hereward, a British destroyer sent by King George VI to take them across the North Sea.
In any case, she arrived in the United Kingdom on 13 May, planning to return to the Netherlands as soon as possible.
The Dutch armed forces in the Netherlands, apart from those in Zeeland, surrendered on 15 May.
In Britain, Queen Wilhelmina took charge of the Dutch government in exile, setting up a chain of command and immediately communicating a message to her people.
Therefore, Wilhelmina sought to remove De Geer from power.
During the war, Queen Wilhelmina's photograph was a sign of resistance against the Germans.
Like Winston Churchill, Wilhelmina broadcast messages to the Dutch people over Radio Oranje.
Queen Wilhelmina visited the United States from 24 June to 11 August 1942 as a guest of the U.S. government.
Shortly afterwards, Wilhelmina went to Canada in 1943 to attend the christening of her new granddaughter Margriet on 29 June 1943 in Ottawa and stayed a while with her family before returning to the United Kingdom.
During the German bombing campaign Operation Steinbock, Queen Wilhelmina was almost killed by a bomb that took the lives of several of her guards and severely damaged her residence near South Mimms in England.
In 1944, Wilhelmina became the first woman since the 15th century, other than queens of the United Kingdom, to be inducted into the Order of the Garter.
Churchill described her as "the only real man among the governments-in-exile" in London.: 146 : 193 


In England, Queen Wilhelmina developed ideas about a new political and social life for the Dutch after the liberation, wanting to create a strong cabinet formed by people active in the resistance.
When the Netherlands was liberated in 1945, the queen was disappointed to see the same political factions taking power as before the war.
In mid-March 1945, she travelled to the liberated areas of the southern Netherlands, visiting the region of Walcheren and the city of Eindhoven where she received a rapturous welcome from the local population.
On 2 May 1945, she went to stay in a small country estate called Anneville located just south of Breda with Juliana and adjuncts Peter Tazelaar, Erik Hazelhoff Roelfzema and fellow Engelandvaarder Rie Stokvis.
Shortly after the war, Queen Wilhelmina wanted to give an award to the Polish Parachute Brigade for their actions during Operation Market Garden and wrote the government a request.
Eventually the Polish Parachute Brigade were awarded the Military Order of William on 31 May 2006, 61 years after Operation Market Garden.
Later years

Following the end of World War II, Queen Wilhelmina made the decision not to return to her palace but to move into a mansion in The Hague, where she lived for eight months.
Around the same time, Queen Wilhelmina's health started failing, forcing her to cede her monarchial duties to Princess Juliana temporarily towards the end of 1947 (14 October – 1 December).
Wilhelmina had every intention of doing so, but exhaustion forced her to relinquish monarchial duties to Juliana again on 12 May 1948, which left the princess to deal with the early elections caused by the ceding of the Indonesian colonies.
Dismayed by the return to pre-war politics and the pending loss of Indonesia, Wilhelmina abdicated on 4 September 1948 after a reign of 57 years and 286 days due to advancing age and illness.
She passed the crown to Juliana and was hence forward styled "Her Royal Highness Princess Wilhelmina of the Netherlands".
No longer queen, Wilhelmina retreated to Het Loo Palace, making few public appearances until the country was devastated by the North Sea flood of 1953.
Wilhelmina died of cardiac arrest in Het Loo Palace at the age of 82 on 28 November 1962.
In popular culture

Titles, styles and honours

Titles and styles

Wilhelmina's full regnal title from her accession to her marriage was: "Wilhelmina, by the Grace of God, Queen of the Netherlands, Princess of Orange-Nassau, Duchess of Limburg, etc."
She adopted her husband's ducal title upon marriage as customary, becoming also a duchess of Mecklenburg.
Honours

Since Wilhelmina received no Dutch honours before ascending the throne aged ten and resigned the position of grand master when she abdicated in 1948, she was in the unusual position of being a Dutch princess and former queen who did not hold a Dutch honour.
Her daughter and successor therefore appointed her Grand Cross of the Military William Order in her first act as Queen.
Foreign

Eponyms

Lèse-majesté case

After Wilhelmina had taken office in 1890, rumours were spread by Socialist satirical magazine De Roode Duivel ("The Red Devil") that William III was not her real father, but Emma's confidant, Sebastiaan Mattheus Sigismund de Ranitz .
References

Sources

External links

2 also Princess of Lippe-Biesterfeld



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c8217a4d-f638-49f7-9555-e366a95564a8)
 Call ID: c8217a4d-f638-49f7-9555-e366a95564a8
  Args:
    source: Wilhelmina
    type: :Person
  AssignClass (369523ff-8a3e-4c94-8dca-ac8e59ae5b12)
 Call ID: 369523ff-8a3e-4c94-8dca-ac8e59ae5b12
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (d754ca09-cd22-4590-8f41-95a621b63791)
 Call ID: d754ca09-cd22-4590-8f41-95a621b63791
  Args:
    type: :Person
    source: William_III
  AssignClass (d06d7395-0dd9-424a-9195-f53cb69edb90)
 Call ID: d06d7395-0dd9-424a-9195-f53cb69edb90
  Args:
    source: William_III
    type: :Man
  AssignClass (8b0dfd22-0b0f-463d-910f-3507bee5e54c)
 Call ID: 8b0dfd22-0b0f-463d-910f-3507bee5e54c
  Args:
    source: Emma
    type: :Person
  AssignClass (1f15bcb0-2778-4b63-b2bb-9324d75b942b)
 Call ID: 1f15bcb0-2778-4b63-b2bb-9324d75b942b
  Args:
    source: Emma
    type: :Woman
  AddTriple (b33d323b-c4ba-4969-898a-ab571d0ea488)
 Call ID: b33d323b-c4ba-4969-898a-ab571d0ea488
  Args:
    target: William_III
    relation: :hasFather
    source: Wilhelmina
  AddTriple (db8198a8-4539-4b0f-8de5-c295cfd43926)
 Call ID: db8198a8-4539-4b0f-8de5-c295cfd43926
  Args:
    target: Emma
    relation: :hasMother
    source: Wilhelmina
  AddLiteral (d07dd133-4405-4b4d-8ca4-8bb05013ed08)
 Call ID: d07dd133-4405-4b4d-8ca4-8bb05013ed08
  Args:
    literal_value: 1880
    relation: :hasBirthYear
    source: Wilhelmina
    literal_type: xsd:integer
  AddLiteral (3d5c573f-bc17-4b9d-b81c-407f1180f0c3)
 Call ID: 3d5c573f-bc17-4b9d-b81c-407f1180f0c3
  Args:
    literal_value: 1962
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Wilhelmina
  AssignClass (30d40730-0e6f-4326-bd0a-029fd26d70f8)
 Call ID: 30d40730-0e6f-4326-bd0a-029fd26d70f8
  Args:
    source: Juliana
    type: :Person
  AssignClass (e1be3eb9-0eea-4926-9a66-7ce82afb5a9f)
 Call ID: e1be3eb9-0eea-4926-9a66-7ce82afb5a9f
  Args:
    source: Juliana
    type: :Woman
  AddTriple (f4e4fad7-431e-402e-a896-309ce282799a)
 Call ID: f4e4fad7-431e-402e-a896-309ce282799a
  Args:
    target: Wilhelmina
    relation: :hasMother
    source: Juliana
  AssignClass (c9bf980b-2d28-4c57-af4d-751b787b3df0)
 Call ID: c9bf980b-2d28-4c57-af4d-751b787b3df0
  Args:
    source: Henry_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (ceae06c6-5d33-4299-ab26-e744164719d2)
 Call ID: ceae06c6-5d33-4299-ab26-e744164719d2
  Args:
    source: Henry_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (e9d980d4-0332-49a7-86c6-cdc84e5f0741)
 Call ID: e9d980d4-0332-49a7-86c6-cdc84e5f0741
  Args:
    target: Henry_of_Mecklenburg-Schwerin
    relation: :hasFather
    source: Juliana
  AddLiteral (d38b8033-bf7e-4f59-9207-2545f359bf98)
 Call ID: d38b8033-bf7e-4f59-9207-2545f359bf98
  Args:
    literal_value: 1901
    relation: :hasMarriageYear
    source: Wilhelmina
    literal_type: xsd:integer
  AddTriple (4d7a68df-7a8f-40fc-a636-9a4d8f8f9fdf)
 Call ID: 4d7a68df-7a8f-40fc-a636-9a4d8f8f9fdf
  Args:
    source: Wilhelmina
    relation: :hasRelation
    target: Henry_of_Mecklenburg-Schwerin
  AssignClass (62c91476-09a7-4f82-9348-4793bb7fddeb)
 Call ID: 62c91476-09a7-4f82-9348-4793bb7fddeb
  Args:
    source: Sophie_of_Württemberg
    type: :Person
  AssignClass (b06c4aa7-b17c-4d22-9b26-bc6384d1921e)
 Call ID: b06c4aa7-b17c-4d22-9b26-bc6384d1921e
  Args:
    source: Sophie_of_Württemberg
    type: :Woman
  AddTriple (f0bf4593-a617-4856-9e5d-3531d6c48276)
 Call ID: f0bf4593-a617-4856-9e5d-3531d6c48276
  Args:
    source: Alexander
    relation: :hasMother
    target: Sophie_of_Württemberg
  AddTriple (b5c07a34-d4d2-438e-966a-37ae12f8b0d4)
 Call ID: b5c07a34-d4d2-438e-966a-37ae12f8b0d4
  Args:
    source: Alexander
    relation: :hasFather
    target: William_III
  AssignClass (20d30e56-2009-4335-870d-20d2d2a3a92c)
 Call ID: 20d30e56-2009-4335-870d-20d2d2a3a92c
  Args:
    source: Alexander
    type: :Person
  AssignClass (31242de4-df32-428c-bbaf-52af9e1dd25f)
 Call ID: 31242de4-df32-428c-bbaf-52af9e1dd25f
  Args:
    source: Alexander
    type: :Man
  AssignClass (55d62729-100f-4536-a6b2-f874c21d1469)
 Call ID: 55d62729-100f-4536-a6b2-f874c21d1469
  Args:
    source: Frederick
    type: :Person
  AssignClass (8733d62e-610a-4f30-822c-514cf3139c48)
 Call ID: 8733d62e-610a-4f30-822c-514cf3139c48
  Args:
    type: :Man
    source: Frederick
  AssignClass (bdb7bd96-2585-4895-8da3-3e8987a447ad)
 Call ID: bdb7bd96-2585-4895-8da3-3e8987a447ad
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (b54ed712-cce8-4cf2-8ff3-041b94ecbaa3)
 Call ID: b54ed712-cce8-4cf2-8ff3-041b94ecbaa3
  Args:
    type: :Man
    source: Bernhard_of_Lippe-Biesterfeld
  AssignClass (40dd1a78-5e7d-42f5-acfa-87f482aa8726)
 Call ID: 40dd1a78-5e7d-42f5-acfa-87f482aa8726
  Args:
    type: :Person
    source: Beatrix
  AssignClass (0e7cf16b-9d62-4134-ac09-ebbd2789650e)
 Call ID: 0e7cf16b-9d62-4134-ac09-ebbd2789650e
  Args:
    source: Beatrix
    type: :Woman
  AddTriple (7de2f52d-aef6-49d4-ba96-91abc1aa0c65)
 Call ID: 7de2f52d-aef6-49d4-ba96-91abc1aa0c65
  Args:
    target: Juliana
    source: Beatrix
    relation: :hasMother
  AssignClass (fccfd823-28e0-45c9-858f-ad22ed9d446f)
 Call ID: fccfd823-28e0-45c9-858f-ad22ed9d446f
  Args:
    type: :Person
    source: Margriet
  AssignClass (2c2c779f-e80b-4f4f-b583-9fc2378c099f)
 Call ID: 2c2c779f-e80b-4f4f-b583-9fc2378c099f
  Args:
    source: Margriet
    type: :Woman
  AddTriple (10e278b7-79b7-4da7-b0cb-0dab40e62562)
 Call ID: 10e278b7-79b7-4da7-b0cb-0dab40e62562
  Args:
    relation: :hasMother
    source: Margriet
    target: Juliana
  Finish (30d63e7e-ce6c-4c7a-bf5c-6d09848052ae)
 Call ID: 30d63e7e-ce6c-4c7a-bf5c-6d09848052ae
  Args: