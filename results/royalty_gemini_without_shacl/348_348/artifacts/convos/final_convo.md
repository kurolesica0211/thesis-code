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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Jaime Bernardo of Bourbon-Parma, Count of Bardi (born 13 October 1972) is a Dutch diplomat and the second son and third child of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
He is a member of the House of Bourbon-Parma as well a member of the extended Dutch royal family.
He was the senior advisor on private sector partnerships at the United Nations High Commissioner for Refugees until 2021 and served as the climate envoy of the Netherlands.
Early life

Jaime was born in Nijmegen, Netherlands.
He has a twin sister, Princess Margarita, who was born one minute earlier.
Besides his twin sister, the prince has one elder brother, Carlos, Duke of Parma, and one younger sister, Princess Carolina.
Prince Jaime was born six weeks prematurely and stayed with his sister in an incubator at the hospital.
Jaime was baptised by Bernardus Johannes Cardinal Alfrink, with his grandfather Prince Bernhard of Lippe-Biesterfeld and his grandmother Princess Madeleine of Bourbon-Parma as his godparents.
Together with his mother and his siblings he moved to the Soestdijk Palace (Baarn), then residence of his grandparents, Queen Juliana and Prince Bernhard, where he lived for several years.
He now works for the Ministry of Foreign Affairs of the Netherlands.
His first role was as the first secretary of the Netherlands Embassy in Baghdad, before becoming a political advisor to the peace mission in Pol-e Khomri in the Baghlan Province in the northern part of Afghanistan.
Until the summer of 2007 the prince worked on secondment in the cabinet of the European Commissioner Neelie Kroes.
On 7 February 2014, the Ministry of Foreign Affairs announced that he would be appointed as ambassador of the Kingdom of the Netherlands to the Holy See.
Prince Jaime was, on 15 July 2014, sworn in as ambassador by King Willem-Alexander and he served till August 2018.
In August 2021 he started as the Climate Envoy of the Netherlands and served for over four years.
The prince performs representative tasks for the Ducal House of Bourbon-Parma.
On 9 November 2015, it was announced that the couple were expecting a second child; daughter Gloria Irene was born on (2016-05-09)9 May 2016.
In a 2015 interview, Princess Viktória stated that the gender of her future child did not matter ("fortunately, we can not influence nature in the terms of gender"), after being told that there were no grandsons for the late Duke of Parma (in April 2016, Jaime's elder brother Carlos, Duke of Parma finally had a son, named Carlos Enrique).
Titles, styles and honours

Titles

Honours

Dynastic honours

Foreign honours

Notes

Already a ducal prince from birth, his father bestowed the substantive title Conte di Bardi ('Count of Bardi') upon him on 2 September 1996.
In 1996 he was incorporated into the Dutch nobility by Queen Beatrix, with the highest noble title Prins de Bourbon de Parme (Prince of Bourbon-Parma), and styled Zijne Koninklijke Hoogheid ('His Royal Highness').
He does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a grandson of Queen Juliana and cousin of the present King Willem-Alexander, he is an official member of the more extended Dutch royal family.
References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (7f2a3fea-c35b-4a96-9917-1fdb0066ac28)
 Call ID: 7f2a3fea-c35b-4a96-9917-1fdb0066ac28
  Args:
    type: :Man
    source: Prince_Felix
  AssignClass (0003da65-1e0c-4a31-a406-265add5906f3)
 Call ID: 0003da65-1e0c-4a31-a406-265add5906f3
  Args:
    source: Prince_Rene
    type: :Man
  AssignClass (9e1ed2fb-4c5b-45e3-891a-25063be169e9)
 Call ID: 9e1ed2fb-4c5b-45e3-891a-25063be169e9
  Args:
    source: Prince_Louis
    type: :Man
  AssignClass (353e511a-d332-4fbb-946a-ecf0d3904ace)
 Call ID: 353e511a-d332-4fbb-946a-ecf0d3904ace
  Args:
    type: :Woman
    source: Princess_Joan
  AssignClass (843b7f8c-2486-4320-b09d-81e8ed80e173)
 Call ID: 843b7f8c-2486-4320-b09d-81e8ed80e173
  Args:
    type: :Woman
    source: Princess_Maria_Pia
  AssignClass (2f6c2ffe-f5eb-4593-883b-d2f9ce55390e)
 Call ID: 2f6c2ffe-f5eb-4593-883b-d2f9ce55390e
  Args:
    source: Princess_Marina
    type: :Woman
  AssignClass (60a8f12c-78ca-40ea-bf3e-f544d4d9ab6e)
 Call ID: 60a8f12c-78ca-40ea-bf3e-f544d4d9ab6e
  Args:
    type: :Man
    source: Prince_Remy
  AssignClass (34059674-f69a-45c2-b43a-405d1681d0d8)
 Call ID: 34059674-f69a-45c2-b43a-405d1681d0d8
  Args:
    source: Princess_Elisabeth
    type: :Woman
  AssignClass (cf253cbb-e4c2-4a0b-843e-fdb70ca5d208)
 Call ID: cf253cbb-e4c2-4a0b-843e-fdb70ca5d208
  Args:
    source: Princess_Chantal
    type: :Woman
  AssignClass (d45a029e-97c8-4985-a408-35344770e559)
 Call ID: d45a029e-97c8-4985-a408-35344770e559
  Args:
    source: Prince_Jean
    type: :Man
  AssignClass (82be778d-a249-4e3f-b614-c6a3d4756c91)
 Call ID: 82be778d-a249-4e3f-b614-c6a3d4756c91
  Args:
    type: :Woman
    source: Princess_Virginia
  AssignClass (89e9b163-3265-4f57-aab0-3e48f6a85722)
 Call ID: 89e9b163-3265-4f57-aab0-3e48f6a85722
  Args:
    source: Princess_Beatrix
    type: :Woman
  AssignClass (e309617e-1121-4dad-ab95-3efbe8f2e2e4)
 Call ID: e309617e-1121-4dad-ab95-3efbe8f2e2e4
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (e5ffb5ee-de79-442a-bf27-8ef7878173c6)
 Call ID: e5ffb5ee-de79-442a-bf27-8ef7878173c6
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (83365cbd-63e9-4c49-9fad-41b28c84df74)
 Call ID: 83365cbd-63e9-4c49-9fad-41b28c84df74
  Args:
    type: :Man
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
  AssignClass (36dda378-02d2-4ac2-8c14-46200a8db22d)
 Call ID: 36dda378-02d2-4ac2-8c14-46200a8db22d
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (2b93268d-7565-4821-9541-8157e4ecd520)
 Call ID: 2b93268d-7565-4821-9541-8157e4ecd520
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (509c48e6-5755-4488-9472-f5f02edefb10)
 Call ID: 509c48e6-5755-4488-9472-f5f02edefb10
  Args:
    source: Princess_Margarita
    type: :Woman
  AssignClass (9fbb3510-61a3-4e46-9ed0-65e7e4145c2e)
 Call ID: 9fbb3510-61a3-4e46-9ed0-65e7e4145c2e
  Args:
    type: :Man
    source: Carlos_Duke_of_Parma
  AssignClass (78145efa-3976-4b40-a2e6-167a53e7b996)
 Call ID: 78145efa-3976-4b40-a2e6-167a53e7b996
  Args:
    source: Princess_Carolina
    type: :Woman
  AssignClass (18e69758-6c8b-438c-94e2-fd04dd325e06)
 Call ID: 18e69758-6c8b-438c-94e2-fd04dd325e06
  Args:
    source: Prince_Bernhard_of_Lippe_Biesterfeld
    type: :Man
  AssignClass (06adf36f-136d-4fdf-8459-cbb661590ff2)
 Call ID: 06adf36f-136d-4fdf-8459-cbb661590ff2
  Args:
    source: Princess_Madeleine_of_Bourbon_Parma
    type: :Woman
  AssignClass (f0da0eff-953d-47b4-843c-86fb203bdd08)
 Call ID: f0da0eff-953d-47b4-843c-86fb203bdd08
  Args:
    type: :Woman
    source: Queen_Juliana
  AssignClass (673174cc-6d28-492e-9c83-78ab3b1fbff7)
 Call ID: 673174cc-6d28-492e-9c83-78ab3b1fbff7
  Args:
    source: Gloria_Irene
    type: :Woman
  AssignClass (d3ee0f6f-2c0b-468b-9ba8-24ef09a0f158)
 Call ID: d3ee0f6f-2c0b-468b-9ba8-24ef09a0f158
  Args:
    type: :Woman
    source: Princess_Viktoria
  AssignClass (4f349b11-29bf-43a3-8ee3-776844854d8e)
 Call ID: 4f349b11-29bf-43a3-8ee3-776844854d8e
  Args:
    type: :Man
    source: Carlos_Enrique
  AddTriple (cb30a536-2a3a-41c9-9fbc-3acb5dac54d8)
 Call ID: cb30a536-2a3a-41c9-9fbc-3acb5dac54d8
  Args:
    relation: :hasChild
    target: Princess_Joan
    source: Prince_Felix
  AddTriple (803986d6-e882-47b4-aa85-a75c99736490)
 Call ID: 803986d6-e882-47b4-aa85-a75c99736490
  Args:
    relation: :hasChild
    target: Princess_Maria_Pia
    source: Prince_Rene
  AddTriple (34ef4735-009c-4f0e-9e56-9bd719e4ddde)
 Call ID: 34ef4735-009c-4f0e-9e56-9bd719e4ddde
  Args:
    source: Prince_Rene
    target: Princess_Marina
    relation: :hasChild
  AddTriple (a27650b1-d5ec-4161-a73d-6e55512a3e78)
 Call ID: a27650b1-d5ec-4161-a73d-6e55512a3e78
  Args:
    source: Prince_Louis
    relation: :hasChild
    target: Prince_Remy
  AddTriple (793a0ae3-5545-4407-b071-1b83d57fb242)
 Call ID: 793a0ae3-5545-4407-b071-1b83d57fb242
  Args:
    target: Princess_Elisabeth
    relation: :hasChild
    source: Prince_Louis
  AddTriple (f025d322-0841-40c8-bac5-40e977bcb03c)
 Call ID: f025d322-0841-40c8-bac5-40e977bcb03c
  Args:
    relation: :hasChild
    target: Princess_Chantal
    source: Prince_Louis
  AddTriple (83115f82-bc7c-4b7d-8ffb-5b7b9a41864f)
 Call ID: 83115f82-bc7c-4b7d-8ffb-5b7b9a41864f
  Args:
    source: Prince_Louis
    target: Prince_Jean
    relation: :hasChild
  AddTriple (91643b61-7ef8-461f-93a9-13b47461f054)
 Call ID: 91643b61-7ef8-461f-93a9-13b47461f054
  Args:
    relation: :hasChild
    target: Princess_Virginia
    source: Prince_Louis
  AddTriple (69179ec8-566d-444e-8124-05f4b077812f)
 Call ID: 69179ec8-566d-444e-8124-05f4b077812f
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    relation: :hasMother
    target: Princess_Irene_of_the_Netherlands
  AddTriple (14376fff-cc17-437c-8676-b3ea8573c0d6)
 Call ID: 14376fff-cc17-437c-8676-b3ea8573c0d6
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    relation: :hasFather
    target: Carlos_Hugo_Duke_of_Parma
  AddLiteral (794bdba0-8ea3-47ae-a623-21eafd039d88)
 Call ID: 794bdba0-8ea3-47ae-a623-21eafd039d88
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    literal_value: 1972
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (90af76d2-eaf5-479a-bcb1-a99015f7e234)
 Call ID: 90af76d2-eaf5-479a-bcb1-a99015f7e234
  Args:
    target: Princess_Margarita
    relation: :isSiblingOf
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
  AddTriple (aade34c6-9ef8-4e77-8f33-141540cb5bd2)
 Call ID: aade34c6-9ef8-4e77-8f33-141540cb5bd2
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    relation: :isSiblingOf
    target: Carlos_Duke_of_Parma
  AddTriple (bb611ff7-89ca-42a7-bb98-bffe5bd6daae)
 Call ID: bb611ff7-89ca-42a7-bb98-bffe5bd6daae
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    target: Princess_Carolina
    relation: :isSiblingOf
  AddTriple (add5a2b0-dee7-4b70-80b3-0f278fe92e93)
 Call ID: add5a2b0-dee7-4b70-80b3-0f278fe92e93
  Args:
    source: Prince_Jaime_Bernardo_of_Bourbon_Parma
    relation: :hasChild
    target: Gloria_Irene
  AddLiteral (b1e9c950-ac01-4836-939e-d387377d1360)
 Call ID: b1e9c950-ac01-4836-939e-d387377d1360
  Args:
    source: Gloria_Irene
    literal_value: 2016-05-09
    literal_type: xsd:date
    relation: :hasBirthYear
  AddTriple (50b0fb43-9d02-408d-af1b-e5f9a7c37ae8)
 Call ID: 50b0fb43-9d02-408d-af1b-e5f9a7c37ae8
  Args:
    source: Carlos_Enrique
    target: Carlos_Duke_of_Parma
    relation: :hasFather
  Finish (e56c4a64-132a-43d4-9030-a54cb91fdfd5)
 Call ID: e56c4a64-132a-43d4-9030-a54cb91fdfd5
  Args: