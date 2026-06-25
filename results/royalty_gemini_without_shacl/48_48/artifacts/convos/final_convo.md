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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4398cbae-982b-4b1d-809e-8731186c0a5c)
 Call ID: 4398cbae-982b-4b1d-809e-8731186c0a5c
  Args:
    type: :Person
    source: :Wilhelmina
  AssignClass (cfe652a4-8435-4da0-a480-75139ed3a2bb)
 Call ID: cfe652a4-8435-4da0-a480-75139ed3a2bb
  Args:
    source: :Wilhelmina
    type: :Woman
  AddLiteral (86559cd3-71b7-4ba7-a06b-de4c5cfc0abc)
 Call ID: 86559cd3-71b7-4ba7-a06b-de4c5cfc0abc
  Args:
    literal_value: 1880
    source: :Wilhelmina
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (78891f32-9007-41e7-b62a-6bef1c858f67)
 Call ID: 78891f32-9007-41e7-b62a-6bef1c858f67
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1962
    source: :Wilhelmina
  AssignClass (3fc5cf75-2c91-49d5-bf9e-11ae2e24d655)
 Call ID: 3fc5cf75-2c91-49d5-bf9e-11ae2e24d655
  Args:
    source: :WilliamIII
    type: :Person
  AssignClass (141b26f6-9a09-48d8-b051-7ba21984c083)
 Call ID: 141b26f6-9a09-48d8-b051-7ba21984c083
  Args:
    source: :WilliamIII
    type: :Man
  AssignClass (8343405c-920d-4a75-8c55-cad5a115aa31)
 Call ID: 8343405c-920d-4a75-8c55-cad5a115aa31
  Args:
    type: :Person
    source: :Emma
  AssignClass (cb5ee035-166f-45d6-9a68-36761f1a6730)
 Call ID: cb5ee035-166f-45d6-9a68-36761f1a6730
  Args:
    source: :Emma
    type: :Woman
  AddTriple (0771e437-e876-4546-a2d5-47fb5bb0a875)
 Call ID: 0771e437-e876-4546-a2d5-47fb5bb0a875
  Args:
    source: :Wilhelmina
    target: :WilliamIII
    relation: :hasFather
  AddTriple (69ffd879-c3b6-4d6a-91b8-5e8d26584047)
 Call ID: 69ffd879-c3b6-4d6a-91b8-5e8d26584047
  Args:
    source: :Wilhelmina
    target: :Emma
    relation: :hasMother
  AssignClass (37f647dc-7e0a-4195-b396-dda6f15d6cd4)
 Call ID: 37f647dc-7e0a-4195-b396-dda6f15d6cd4
  Args:
    type: :Person
    source: :Henry
  AssignClass (8b9b6889-c92f-4672-b91e-4fe2540d3562)
 Call ID: 8b9b6889-c92f-4672-b91e-4fe2540d3562
  Args:
    type: :Man
    source: :Henry
  AddTriple (0ec1cf35-affc-4b08-b10d-c08cbed64f31)
 Call ID: 0ec1cf35-affc-4b08-b10d-c08cbed64f31
  Args:
    relation: :hasRelation
    target: :Henry
    source: :Wilhelmina
  AddLiteral (3ad1fa88-d9f4-4985-b5af-a873a366e1da)
 Call ID: 3ad1fa88-d9f4-4985-b5af-a873a366e1da
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1901
    source: :Wilhelmina
  AssignClass (89c95508-19b1-4994-a884-ed3e7d4731a7)
 Call ID: 89c95508-19b1-4994-a884-ed3e7d4731a7
  Args:
    source: :Juliana
    type: :Person
  AssignClass (c03b6524-7b9d-4b04-b06e-4b05ffd2857f)
 Call ID: c03b6524-7b9d-4b04-b06e-4b05ffd2857f
  Args:
    type: :Woman
    source: :Juliana
  AddTriple (fbc62550-f080-4820-8bc5-78ef7d2e6ea0)
 Call ID: fbc62550-f080-4820-8bc5-78ef7d2e6ea0
  Args:
    relation: :hasMother
    source: :Juliana
    target: :Wilhelmina
  AddTriple (7ba429af-5e87-496b-b444-9a5c64ef3970)
 Call ID: 7ba429af-5e87-496b-b444-9a5c64ef3970
  Args:
    source: :Juliana
    target: :Henry
    relation: :hasFather
  AssignClass (3522126d-0d6f-46c6-9b8b-c8f4a75492b2)
 Call ID: 3522126d-0d6f-46c6-9b8b-c8f4a75492b2
  Args:
    source: :Beatrix
    type: :Person
  AssignClass (4f732d92-a099-4a6d-acde-e960c165806e)
 Call ID: 4f732d92-a099-4a6d-acde-e960c165806e
  Args:
    type: :Woman
    source: :Beatrix
  AddTriple (96ff239d-2cfa-43e0-bc9a-219694ba959b)
 Call ID: 96ff239d-2cfa-43e0-bc9a-219694ba959b
  Args:
    relation: :hasMother
    target: :Juliana
    source: :Beatrix
  AssignClass (209c7178-1992-4ef0-a995-ba7aff917d1d)
 Call ID: 209c7178-1992-4ef0-a995-ba7aff917d1d
  Args:
    type: :Person
    source: :Margriet
  AssignClass (991c23ac-642a-4242-a4ca-ec58f2367b68)
 Call ID: 991c23ac-642a-4242-a4ca-ec58f2367b68
  Args:
    source: :Margriet
    type: :Woman
  AddTriple (aee939e9-cbae-4a07-be46-6d36fe65bf7e)
 Call ID: aee939e9-cbae-4a07-be46-6d36fe65bf7e
  Args:
    target: :Juliana
    source: :Margriet
    relation: :hasMother
  AssignClass (ea6dc7d6-adc7-4cfe-809e-ce0925500545)
 Call ID: ea6dc7d6-adc7-4cfe-809e-ce0925500545
  Args:
    source: :Sophie
    type: :Person
  AssignClass (441dda57-98f1-44e5-b628-cb2c0a1daf08)
 Call ID: 441dda57-98f1-44e5-b628-cb2c0a1daf08
  Args:
    type: :Woman
    source: :Sophie
  AddTriple (67acda60-95f6-4fd2-b3c7-b071b85d9ac7)
 Call ID: 67acda60-95f6-4fd2-b3c7-b071b85d9ac7
  Args:
    source: :WilliamIII
    target: :Sophie
    relation: :hasRelation
  AssignClass (717c61a2-5dae-43c0-83ab-8b3c28f31abf)
 Call ID: 717c61a2-5dae-43c0-83ab-8b3c28f31abf
  Args:
    source: :Alexander
    type: :Person
  AssignClass (e5cf0cb8-210b-4ea5-9c48-787f38be80a2)
 Call ID: e5cf0cb8-210b-4ea5-9c48-787f38be80a2
  Args:
    type: :Man
    source: :Alexander
  AddTriple (44564210-b1dd-453f-a7b4-a8ec7a35dc73)
 Call ID: 44564210-b1dd-453f-a7b4-a8ec7a35dc73
  Args:
    relation: :hasFather
    target: :WilliamIII
    source: :Alexander
  AddTriple (fd31af31-a1d6-4958-a0dc-2d89869bc4c1)
 Call ID: fd31af31-a1d6-4958-a0dc-2d89869bc4c1
  Args:
    relation: :hasMother
    source: :Alexander
    target: :Sophie
  AssignClass (e112fec7-e056-42d5-8b26-dec2abfde078)
 Call ID: e112fec7-e056-42d5-8b26-dec2abfde078
  Args:
    source: :Frederick
    type: :Person
  AssignClass (82272061-3ccc-46b4-94b6-2d3d4f9d3b73)
 Call ID: 82272061-3ccc-46b4-94b6-2d3d4f9d3b73
  Args:
    type: :Man
    source: :Frederick
  Finish (ffa319fd-619b-4303-9b89-7ab21bf1eb61)
 Call ID: ffa319fd-619b-4303-9b89-7ab21bf1eb61
  Args: