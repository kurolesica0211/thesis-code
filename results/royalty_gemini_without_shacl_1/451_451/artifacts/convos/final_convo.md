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
Heinrich XIII Prinz Reuss (German: Heinrich XIII.
Prinz Reuß, .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}pronounced ; born 4 December 1951) is a German businessman, far-right and monarchist activist, and member of the aristocratic – formerly sovereign – House of Reuss.
A proponent of the Reichsbürger movement and antisemitic conspiracy theories, Reuss was arrested by German Federal Police in December 2022 due to his alleged leadership in the 2022 German coup d'état plot.
Biography

Personal life and ancestry

Reuss was born in Büdingen on 4 December 1951, the fifth of six children and the fourth son born to Prince Heinrich I Reuss and Duchess Woizlawa Feodora of Mecklenburg, who was in turn the only child of the German colonial governor Duke Adolf Friedrich of Mecklenburg.
Reuss's parents, like all German nobility, had become private citizens in 1919 upon the adoption of the Weimar Constitution, which abolished any privileges and titles that had previously existed for nobility.
The House of Reuss, from which Reuss is descended, dates to the 12th century and historically administered the regions of Gera and Greiz, a non-contiguous mini-state in what is today Eastern Thuringia.
Reuss left the family association at his own request around 2009.
Reuss married Iranian-born Susan Doukht Jalali in 1989, and they have two children, including a son named Heinrich XXVIII (born circa 1991) and a daughter Elena, who has Down syndrome and was born in 1989.
His wife uses the name Princess Susan Reuss and works as a naturopath.
Reuss is also reported to have as a girlfriend a Russian national identified by prosecutors as "Vitalia B.", aged 39 in 2022, at their arrest who allegedly had some role in the coup plot.
Business and family activities

Reuss worked as a real estate developer, operating a company named Büro Prinz Reuss in Frankfurt, and also produced sparkling wine.
In 1945, the Communist land reform in the Soviet occupation zone (East Germany) expropriated all movable and immovable assets of the House of Reuss.
Following the reunification of Germany in 1990, Reuss tried to have properties restituted.
The clan, which consisted of five large families, wanted Gera townhouses, four castles, extensive forestry and agricultural property and the Jugendstil Reuss Theater in Gera, then held by the city of Gera in Thuringia.
Concerning the theater, Reuss and the mayor of Gera were unable to negotiate a settlement, each blaming the other.
Reuss spent much of his fortune on lawsuits seeking restitution, but with little success.
In 2017, he supported the reinterment of the remains of a number of his ancestors, most prominent among them Henry II, Count of Reuss-Gera, in their original location.
Views and conspiracy theories

Many of Reuss's views are consistent with monarchism.
He has spoken in favour of low flat tax for all citizens and against debt-based business models hailing the 10 percent rate in the former Principality of Reuss, saying it let Reuss's citizens lead "happy lives" because it was "straightforward and transparent".
Reuss contended that the modern German government and European Union were more distant and inaccessible than feudal princes.
Reuss also gave speeches claiming that Germany had been a vassal state since the Second World War.
At World Web Forum in Zürich in 2019, Reuss gave a speech accusing the Rothschilds and Freemasons of responsibility for the wars of the 20th century, expressing antisemitic conspiracy theories.
On 22 December 2018, Reuss and his mother attended the unveiling of a "Flame of Peace" sculpture in Gera in honor of her 100th birthday by the heads of the Vienna-based Association for the Promotion of Peace.
In 2020, Reuss participated in the celebration of the first International Day of Conscience event in Vienna.
Assault on journalist Peter Hagen

In August 2022, Reuss attended an official reception held by Thomas Weigelt, the mayor of Bad Lobenstein, where Reuss's hunting lodge Jagdschloss Waidmannsheil  is located.
Weigelt was known to be sympathetic to the Reichsbürger movement and journalist Peter Hagen asked him why someone associated with the Reichsbürger scene like Reuss would be invited to an official event.
The next day Hagen approached the mayor at the market festival and tried to film him in familiar conversation with Reuss and AfD-politician Uwe Thrum.
Afterwards, the current head of the Reuss family, Heinrich XIV Fürst Reuss , objected to his involvement in local politics "in the strongest possible way".
He called Heinrich XIII, his third cousin, a "distant relative" and "a confused old man peddling in conspiracy theories".
Involvement in 2022 German coup plot

On 7 December 2022, Reuss was arrested at his home in the Westend district of Frankfurt during an extensive raid of alleged far-right conspirators planning a coup d'état.
According to police, the coup's conspirators—which included former Bundestag member Birgit Malsack-Winkemann—were proponents of the Reichsbürger movement who hoped to install the 71-year-old Reuss as head of state Reuss's hunting lodge Jagdschloss Waidmannsheil  in Saaldorf , Thuringia was allegedly the site of weapons stockpiles and meetings regarding the conspiracy.
Reuss and "Vitalia B." are reported to have reached out to the Russian government via its Consulate General in Leipzig, presumably for assistance in the coup.
Heinrich XIV Fürst Reuss distanced himself and his family again after Reuss was arrested in 2022, calling Reuss a "confused old man" and "a marginal figure" and noting that their last common ancestor lived in the early 19th century.
He said Reuss's behaviour was a "catastrophe" for the family, whose heritage as tolerant and cosmopolitan rulers was now associated with "terrorists and reactionaries".
He believes Reuss's anti-government views derive from his resentment at the German judicial system for its failure to recognize his claims to family properties expropriated at the end of World War II.
The trial of Reuss and eight other plotters began on 21 May 2024 in Frankfurt.



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
  AssignClass (3be357e7-517e-40f2-8329-67277df85b1b)
 Call ID: 3be357e7-517e-40f2-8329-67277df85b1b
  Args:
    source: Heinrich_XIII_Prinz_Reuss
    type: :Man
  AssignClass (69f86ece-2298-4819-bf92-8ae3354b1ca3)
 Call ID: 69f86ece-2298-4819-bf92-8ae3354b1ca3
  Args:
    type: :Man
    source: Heinrich_I_Reuss
  AssignClass (6e4f4c31-e8f5-4251-9511-87694e550179)
 Call ID: 6e4f4c31-e8f5-4251-9511-87694e550179
  Args:
    source: Woizlawa_Feodora_of_Mecklenburg
    type: :Woman
  AssignClass (63e9f0c4-ae4e-431f-b650-6c03f3b2fa72)
 Call ID: 63e9f0c4-ae4e-431f-b650-6c03f3b2fa72
  Args:
    source: Adolf_Friedrich_of_Mecklenburg
    type: :Man
  AssignClass (9c4fc070-907f-43dd-86bd-e34c7adbdda8)
 Call ID: 9c4fc070-907f-43dd-86bd-e34c7adbdda8
  Args:
    source: Susan_Doukht_Jalali
    type: :Woman
  AssignClass (07fbea85-6cb4-460b-9741-19175cb610a5)
 Call ID: 07fbea85-6cb4-460b-9741-19175cb610a5
  Args:
    source: Heinrich_XXVIII
    type: :Man
  AssignClass (e07ff452-09d9-4825-95b1-20c0e7f8ede5)
 Call ID: e07ff452-09d9-4825-95b1-20c0e7f8ede5
  Args:
    source: Elena
    type: :Woman
  AssignClass (f81caf31-9d45-4959-b5bf-004b622ea002)
 Call ID: f81caf31-9d45-4959-b5bf-004b622ea002
  Args:
    source: Vitalia_B
    type: :Woman
  AssignClass (26b904c4-bfd1-4123-b9ba-91d8d9c570b3)
 Call ID: 26b904c4-bfd1-4123-b9ba-91d8d9c570b3
  Args:
    type: :Man
    source: Heinrich_XIV_Fuerst_Reuss
  AssignClass (c6ea4e9a-7b6c-457b-a3bb-2a272144ba96)
 Call ID: c6ea4e9a-7b6c-457b-a3bb-2a272144ba96
  Args:
    source: Henry_II_Count_of_Reuss_Gera
    type: :Man
  AddLiteral (ebb64ee3-a201-45de-ab4a-0dbfc039f08c)
 Call ID: ebb64ee3-a201-45de-ab4a-0dbfc039f08c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1951
    source: Heinrich_XIII_Prinz_Reuss
  AddTriple (03e33f64-8fb1-4b82-a420-fee15be0397a)
 Call ID: 03e33f64-8fb1-4b82-a420-fee15be0397a
  Args:
    target: Heinrich_I_Reuss
    relation: :hasFather
    source: Heinrich_XIII_Prinz_Reuss
  AddTriple (9bbdf8b6-e775-4a3c-8ac4-40dca6710893)
 Call ID: 9bbdf8b6-e775-4a3c-8ac4-40dca6710893
  Args:
    target: Woizlawa_Feodora_of_Mecklenburg
    relation: :hasMother
    source: Heinrich_XIII_Prinz_Reuss
  AddTriple (383d591c-e4af-4b3c-9d68-be83dc1c537e)
 Call ID: 383d591c-e4af-4b3c-9d68-be83dc1c537e
  Args:
    relation: :hasFather
    target: Adolf_Friedrich_of_Mecklenburg
    source: Woizlawa_Feodora_of_Mecklenburg
  AddTriple (fcaaa6a7-9d8d-4685-9f5d-23cb90a12f6c)
 Call ID: fcaaa6a7-9d8d-4685-9f5d-23cb90a12f6c
  Args:
    relation: :hasFather
    target: Susan_Doukht_Jalali
    source: Heinrich_XIII_Prinz_Reuss
  AddTriple (25d41276-96e1-4b25-a133-2a9806121099)
 Call ID: 25d41276-96e1-4b25-a133-2a9806121099
  Args:
    source: Heinrich_XIII_Prinz_Reuss
    target: Heinrich_XXVIII
    relation: :hasSon
  AddTriple (39d14121-73bc-46ce-8bc2-e01f41a83e83)
 Call ID: 39d14121-73bc-46ce-8bc2-e01f41a83e83
  Args:
    source: Heinrich_XIII_Prinz_Reuss
    relation: :hasDaughter
    target: Elena
  AddTriple (ae77d588-2f40-4590-8157-475041cecdf6)
 Call ID: ae77d588-2f40-4590-8157-475041cecdf6
  Args:
    source: Heinrich_XXVIII
    relation: :hasMother
    target: Susan_Doukht_Jalali
  AddTriple (b8df007e-d8bc-497d-b99f-a6b59f1eaf27)
 Call ID: b8df007e-d8bc-497d-b99f-a6b59f1eaf27
  Args:
    target: Susan_Doukht_Jalali
    relation: :hasMother
    source: Elena
  AddTriple (39869c13-6a74-4dd7-9263-568b0cd8ae71)
 Call ID: 39869c13-6a74-4dd7-9263-568b0cd8ae71
  Args:
    source: Heinrich_XIII_Prinz_Reuss
    target: Henry_II_Count_of_Reuss_Gera
    relation: :hasAncestor
  Finish (ebf92b98-383f-4e1f-a34c-307fa081f6e5)
 Call ID: ebf92b98-383f-4e1f-a34c-307fa081f6e5
  Args: