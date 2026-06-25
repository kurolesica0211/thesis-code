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
Frederick Francis IV (Friedrich Franz Michael; 9 April 1882 – 17 November 1945) was the last Grand Duke of Mecklenburg-Schwerin and regent of Mecklenburg-Strelitz.
Early life

Born on 9 April 1882, Duke Frederick Francis IV was the son of Frederick Francis, then the hereditary grand duke of Mecklenburg-Schwerin, and Grand Duchess Anastasia Mikhailovna of Russia.
He was born in Palermo, Sicily at Villa Belmonte where his parents were staying to alleviate the faltering health of the hereditary Grand duke.
Frederick Francis's father suffered from a weak heart, chronic asthma, and acute eczema and had to live part of the year away from Mecklenburg in a warmer climate.
Frederick Francis's mother, raised in the splendor of the Russian imperial court and the Orthodox church, never got used to the provincial austerity of the Lutheran court of Schwerin, preferring to live abroad.
Frederick Francis was one year old when he became the hereditary grand duke of Mecklenburg-Schwerin at the death of his grandfather Grand Duke Frederick Francis II on 15 April 1883.
Frederick Francis IV had an older sister, Alexandrine and a younger one, Cecilie.
Friederich Franz III spent most his time hunting, while Anastasia and the children rode or drove out, visited local people or enjoyed the beach and the surrounding forest.
Grand Duke of Mecklenburg-Schwerin

Frederick Francis IV succeeded his father as Grand Duke upon his death on 10 April 1897.
As he was a teenager, due to his minority, the grand duchy was governed by his uncle Duke Johann Albrecht as regent.
Frederick Francis's mother, Grand Duchess Anastasia preferred to remain in France while he continued the long preparation to eventually assume the throne.
In 1903, the young Grand Duke moved to Bonn, where he attended university and studied administration and law.
On 9 April 1901 Frederick Francis came of age, ending the regency and beginning his reign in Schwerin.
Marriage and issue

On 7 June 1904, Frederick Francis married Princess Alexandra of Hanover in Gmunden.
She was the second eldest daughter of Ernest Augustus, Crown Prince of Hanover, and his wife, Princess Thyra of Denmark, a daughter of King Christian IX.
They had five children:


Abdication

Following the 1918 suicide of Grand Duke Adolphus Frederick VI of Mecklenburg-Strelitz, Frederick Francis took up the regency of Strelitz.
Frederick Francis abdicated the grand ducal throne on 14 November 1918 following the German Empire's defeat in World War I; the regency over the Grand Duchy of Mecklenburg-Strelitz ended at the same time.
Frederick Francis died on 17 November 1945 in Flensburg, at the age of 63, after being arrested by No6 RAF Security section on 9 November 1945.
He was succeeded as head of the grand ducal house by his son Hereditary Grand Duke Friedrich Franz.



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
  AssignClass (8a893c58-c5b6-47e9-bea7-399908fec5ed)
 Call ID: 8a893c58-c5b6-47e9-bea7-399908fec5ed
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (20d16cad-9304-4d8b-8d60-c50dd4b22622)
 Call ID: 20d16cad-9304-4d8b-8d60-c50dd4b22622
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AddLiteral (e9ea3502-6150-487e-b21e-8dd631876827)
 Call ID: e9ea3502-6150-487e-b21e-8dd631876827
  Args:
    source: Frederick_Francis_IV
    literal_value: 1882
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (33d73749-bf97-4b33-9259-0c1e89fc88cf)
 Call ID: 33d73749-bf97-4b33-9259-0c1e89fc88cf
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1945
    source: Frederick_Francis_IV
  AssignClass (d7b4933a-ad2c-488e-8533-1875e6ca4bee)
 Call ID: d7b4933a-ad2c-488e-8533-1875e6ca4bee
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (cef69d05-1da1-471f-a121-16afe79b7d44)
 Call ID: cef69d05-1da1-471f-a121-16afe79b7d44
  Args:
    source: Frederick_Francis_III
    type: :Person
  AssignClass (7741cbed-2a48-4f99-b561-6c28d25369cd)
 Call ID: 7741cbed-2a48-4f99-b561-6c28d25369cd
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna
  AssignClass (c35f2d98-4fe3-4aaf-b50f-17431edefa3c)
 Call ID: c35f2d98-4fe3-4aaf-b50f-17431edefa3c
  Args:
    source: Anastasia_Mikhailovna
    type: :Person
  AddTriple (8c18346d-924b-432c-8316-d1946489bb73)
 Call ID: 8c18346d-924b-432c-8316-d1946489bb73
  Args:
    relation: :hasFather
    target: Frederick_Francis_III
    source: Frederick_Francis_IV
  AddTriple (f774332f-f412-42e5-9974-6e2387b5b536)
 Call ID: f774332f-f412-42e5-9974-6e2387b5b536
  Args:
    source: Frederick_Francis_IV
    target: Anastasia_Mikhailovna
    relation: :hasMother
  AssignClass (8a0f7c8e-9e09-46a1-8bdb-1a676ab427d1)
 Call ID: 8a0f7c8e-9e09-46a1-8bdb-1a676ab427d1
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (4c9190c1-d317-4106-8742-7749b7841e9c)
 Call ID: 4c9190c1-d317-4106-8742-7749b7841e9c
  Args:
    type: :Person
    source: Frederick_Francis_II
  AddTriple (a7e317be-591a-4c86-b465-3f3f3625e221)
 Call ID: a7e317be-591a-4c86-b465-3f3f3625e221
  Args:
    relation: :isFatherOf
    target: Frederick_Francis_III
    source: Frederick_Francis_II
  AssignClass (80d5dff7-bec2-46e9-9a8a-abb3a93e867f)
 Call ID: 80d5dff7-bec2-46e9-9a8a-abb3a93e867f
  Args:
    source: Alexandrine
    type: :Woman
  AssignClass (aee0805a-5099-46b1-b832-e502833a5970)
 Call ID: aee0805a-5099-46b1-b832-e502833a5970
  Args:
    source: Alexandrine
    type: :Person
  AssignClass (5c25f5f2-e2e8-407b-a7d8-9b331db743bf)
 Call ID: 5c25f5f2-e2e8-407b-a7d8-9b331db743bf
  Args:
    type: :Woman
    source: Cecilie
  AssignClass (dd416ec0-8186-4877-8395-12cd96a59156)
 Call ID: dd416ec0-8186-4877-8395-12cd96a59156
  Args:
    source: Cecilie
    type: :Person
  AddTriple (b2de7aba-2847-4f84-82c6-a7f36e71f82a)
 Call ID: b2de7aba-2847-4f84-82c6-a7f36e71f82a
  Args:
    source: Frederick_Francis_IV
    relation: :isSiblingOf
    target: Alexandrine
  AddTriple (20549089-9f7b-4347-b35a-1fd6d8705e3a)
 Call ID: 20549089-9f7b-4347-b35a-1fd6d8705e3a
  Args:
    relation: :isSiblingOf
    target: Cecilie
    source: Frederick_Francis_IV
  AssignClass (4b5bf3e1-e667-46d4-8e97-86efca12b796)
 Call ID: 4b5bf3e1-e667-46d4-8e97-86efca12b796
  Args:
    source: Johann_Albrecht
    type: :Man
  AssignClass (0fefbd90-b4ee-4855-84b9-7781d5e595bd)
 Call ID: 0fefbd90-b4ee-4855-84b9-7781d5e595bd
  Args:
    type: :Person
    source: Johann_Albrecht
  AddTriple (fa424eb2-5995-449d-99c5-4ffcde93d72a)
 Call ID: fa424eb2-5995-449d-99c5-4ffcde93d72a
  Args:
    source: Johann_Albrecht
    relation: :isSiblingOf
    target: Frederick_Francis_III
  AssignClass (066d8bdc-0456-4340-8c42-864e9f626303)
 Call ID: 066d8bdc-0456-4340-8c42-864e9f626303
  Args:
    type: :Woman
    source: Alexandra_of_Hanover
  AssignClass (a671b812-49d5-4716-8827-3f8d8b1abd8d)
 Call ID: a671b812-49d5-4716-8827-3f8d8b1abd8d
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddTriple (b3563e3f-1628-4fb1-9e83-047e54e90476)
 Call ID: b3563e3f-1628-4fb1-9e83-047e54e90476
  Args:
    source: Frederick_Francis_IV
    target: Alexandra_of_Hanover
    relation: :hasRelation
  AddLiteral (6eee95f3-84a1-4448-956a-8c44d5ce252e)
 Call ID: 6eee95f3-84a1-4448-956a-8c44d5ce252e
  Args:
    literal_value: 1904
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Frederick_Francis_IV
  AssignClass (b787b166-1683-4d0e-be7f-bac8d623be4d)
 Call ID: b787b166-1683-4d0e-be7f-bac8d623be4d
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (2f47b1ff-351c-4ffd-b5a1-a17fd9ff5066)
 Call ID: 2f47b1ff-351c-4ffd-b5a1-a17fd9ff5066
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Person
  AssignClass (37599843-02ad-4fd2-a171-3b1475fec9ad)
 Call ID: 37599843-02ad-4fd2-a171-3b1475fec9ad
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (d55483fb-baa2-40a3-9322-65b26467caf9)
 Call ID: d55483fb-baa2-40a3-9322-65b26467caf9
  Args:
    type: :Person
    source: Thyra_of_Denmark
  AddTriple (06f2f7a2-aef4-4fd7-ac1f-5ec9adf7c828)
 Call ID: 06f2f7a2-aef4-4fd7-ac1f-5ec9adf7c828
  Args:
    source: Alexandra_of_Hanover
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (f2659fc2-ba79-4eaa-8139-ec446032660f)
 Call ID: f2659fc2-ba79-4eaa-8139-ec446032660f
  Args:
    source: Alexandra_of_Hanover
    target: Thyra_of_Denmark
    relation: :hasMother
  AssignClass (5c1a41b5-8cb1-477a-8195-d49832566a42)
 Call ID: 5c1a41b5-8cb1-477a-8195-d49832566a42
  Args:
    source: Christian_IX
    type: :Man
  AssignClass (3b6060f1-d8e4-436b-8e4b-e27e584f13cc)
 Call ID: 3b6060f1-d8e4-436b-8e4b-e27e584f13cc
  Args:
    type: :Person
    source: Christian_IX
  AddTriple (e5b2f4f3-694a-4cb7-a8c1-93c1ee1a75d0)
 Call ID: e5b2f4f3-694a-4cb7-a8c1-93c1ee1a75d0
  Args:
    relation: :isFatherOf
    target: Thyra_of_Denmark
    source: Christian_IX
  AssignClass (398ce1b9-6099-4eaa-a6da-c69f675da066)
 Call ID: 398ce1b9-6099-4eaa-a6da-c69f675da066
  Args:
    source: Adolphus_Frederick_VI
    type: :Man
  AssignClass (8b27a0e8-6ed1-43cd-9295-0db57868612b)
 Call ID: 8b27a0e8-6ed1-43cd-9295-0db57868612b
  Args:
    source: Adolphus_Frederick_VI
    type: :Person
  AssignClass (e081dc22-0070-4f08-94bc-43834d3bcd44)
 Call ID: e081dc22-0070-4f08-94bc-43834d3bcd44
  Args:
    type: :Man
    source: Friedrich_Franz_son
  AssignClass (5ca63a6b-23e4-4462-8fbf-c7291d1dab99)
 Call ID: 5ca63a6b-23e4-4462-8fbf-c7291d1dab99
  Args:
    source: Friedrich_Franz_son
    type: :Person
  AddTriple (6ee51933-2eab-4ce9-96f9-362f2192d5dd)
 Call ID: 6ee51933-2eab-4ce9-96f9-362f2192d5dd
  Args:
    source: Frederick_Francis_IV
    target: Friedrich_Franz_son
    relation: :hasSon
  Finish (7c78e161-9744-466c-ab94-5b9f33ee4b04)
 Call ID: 7c78e161-9744-466c-ab94-5b9f33ee4b04
  Args: