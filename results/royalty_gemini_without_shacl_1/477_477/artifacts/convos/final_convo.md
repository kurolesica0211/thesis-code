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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Alexander, Crown Prince of Yugoslavia (Serbian: Александар Карађорђевић, Престолонаследник Југославије, romanized: Aleksandar Karađorđević, Prestolonaslednik Jugoslavije; born 17 July 1945), is the head of the House of Karađorđević, the former royal house of the defunct Kingdom of Yugoslavia and its predecessor the Kingdom of Serbia.
Alexander is the only child of King Peter II and Princess Alexandra of Greece and Denmark.
He held the position of crown prince in the Democratic Federal Yugoslavia for the first four-and-a-half months of his life, until the declaration of the Federal People's Republic of Yugoslavia later in November 1945, when the monarchy was abolished.
In public he claims the crowned royal title of "Alexander II Karadjordjevic" (Serbian: Александар II Карађорђевић, Aleksandar II Karađorđević) as a pretender to the throne.
Through his father, Alexander is a direct descendant of Queen Victoria, through his great-great-grandfather Prince Alfred, Duke of Saxe-Coburg and Gotha, Victoria's second eldest son.
Alexander is known for his support of constitutional monarchism and his humanitarian work.
He left Yugoslavia in April 1941 and arrived in London in June 1941.
Commenting on the event and what happened to his father, Crown Prince Alexander said, "He  was too straight.
On 29 November 1943, AVNOJ (formed by the Partisans) declared themselves the sovereign communist government of Yugoslavia and announced that they would take away all legal rights from the Royal government.
On 10 August 1945, less than a month after Alexander's birth, AVNOJ named the country Democratic Federal Yugoslavia.
On 29 November 1945, the country was declared a communist republic and changed its name to People's Federal Republic of Yugoslavia.
In 1947, all members of Alexander's family except for his granduncle Prince George were deprived of their Yugoslav citizenship and their property was confiscated.
As of 8 July 2015, the High Court in Belgrade found that decree 392, issued by the Presidency of the Presidium of the National Assembly on 3 August 1947, which deprived King Peter II and other members of the House of Karađorđević of their citizenship, was null and void from the moment of its adoption, in the parts pertaining to Crown Prince Alexander, and that all of its legal consequences are thus null and void.
Birth and childhood

Alexander was born in Suite 212 of Claridge's Hotel in Brook Street, Mayfair, London, on 17 July 1945.
The British Government is said to have temporarily ceded sovereignty over the suite in which the birth occurred to Yugoslavia so that the crown prince would be born on Yugoslav territory, though the story may be apocryphal, as there exists no documentary record of this.
Another part of the story says that a box of soil from the homeland was placed under the bed, so the Prince could be born on Yugoslav soil.
It is now Suite 214 and known as the 'Alexander Suite'.
He was the only child of King Peter II and Queen Alexandra of Yugoslavia.
His parents were relatively unable to take care of him due to their various health and financial problems, so Alexander was raised by his maternal grandmother, Princess Aspasia of Greece and Denmark.
Military service

Alexander graduated from the Royal Military Academy Sandhurst in 1966 and was commissioned as an officer into the British Army's 16th/5th The Queen's Royal Lancers regiment, rising to the rank of captain.
After leaving the army in 1972, Alexander, who speaks several languages, pursued a career in international business.
, he married Princess Maria da Gloria of Orléans-Braganza (b. 1946) from the Brazilian imperial family, at the parish church of St. Mary Magdalene.
They are double 4th cousins once removed as both are descendants of Prince Ferdinand of Saxe-Coburg and Gotha (1785–1851) and Princess Maria Antonia von Koháry (1797–1862), as well as of Pedro I, Emperor of Brazil and Archduchess Maria Leopoldina of Austria.
They have three sons: Peter (born 5 February 1980), and fraternal twins: Philip and Alexander (both born 15 January 1982).
Alexander and Maria da Gloria divorced on 19 February 1985.
Maria da Gloria married Ignacio de Medina, Duke of Segorbe (b. 1947), while Crown Prince Alexander married Katherine Clairy Batis, daughter of Robert Batis and Anna Dosti, civilly on 20 September 1985, and religiously the following day, at St. Sava Serbian Orthodox Church, Notting Hill, London.
Since their marriage, she is known as Crown Princess Katherine, as per the royal family's website.
On 16 December 2017, Alexander attended with his wife the state funeral of his first cousin once removed, King Michael of Romania in Bucharest, along with other heads of European royal families and invited guests.
On 19 September 2022, Crown Prince Alexander and his wife Katherine attended the state funeral of his godmother Queen Elizabeth II.
On 6 February 2024, following the news about King Charles' health, Alexander himself revealed that he had been treated for early stage prostate cancer in December 2023.
Return to Yugoslavia

Alexander first came to Yugoslavia in 1991.
He actively worked with the opposition to Slobodan Milošević and moved to Yugoslavia after Milošević had been deposed in 2000.
On 27 February 2001, the parliament of the Federal Republic of Yugoslavia (FRY) passed legislation conferring citizenship on members of the Karađorđević family.
The legislation may also have effectively annulled a decree stripping the family of its citizenship of the Socialist Federal Republic of Yugoslavia (SFRY) in 1947.
Belief in constitutional monarchy

Alexander is a proponent of re-creating a constitutional monarchy in Serbia and sees himself as the rightful king.
He believes that monarchy could give Serbia "stability, continuity and unity".
A number of political parties and organizations support a constitutional parliamentary monarchy in Serbia.
The assassinated former Serbian Prime Minister Zoran Đinđić was often seen in the company of the prince and his family, supporting their campaigns and projects, although his Democratic Party never publicly embraced monarchism.
Crown Prince Alexander has vowed to stay out of politics.
He and Princess Katherine spend considerable time engaging in humanitarian work.
The Crown Prince has, however, increasingly participated in public functions alongside the leaders of Serbia, the former Yugoslav republics and members of the diplomatic corps.
On 11 May 2006, he hosted a reception at the Royal Palace for delegates attending a summit on Serbia and Montenegro.
The reception was attended by the Governor of the National Bank of Serbia, as well as ambassadors and diplomats from Slovenia, Poland, Brazil, Japan, the United States, and Austria.
In addition, we in Serbia and Montenegro must take into account that whatever form we take within the European Union, we have only but one choice and that is to work for the common good of all member nations.
It is also central to take into account that stability in our region will be enhanced when Serbia is fully at peace with itself.
The Crown Prince raised the issue of a royal restoration in the immediate aftermath of the vote.
I strongly believe in a Constitutional Parliamentary Kingdom of Serbia.
Again, we need to be proud, a strong Serbia that is at peace with itself and with its neighbors.
Only if we have a form of governance close to the Serbian soul: the Kingdom of Serbia.
What is most important is the interest of Serbia.
I am ready to meet all our politicians; we have to work together for the common good of Serbia, and to be friends in the name of the future of our country.
I appeal for mature democratic debate in the interest of Serbia.
Serbia must have clear and realistic objectives.
The public also had reservations with Alexander's apparent lack of knowledge of the Serbian language.
On 27 July 2015, newspaper Blic published a poll "Da li Srbija treba da bude monarhija?" ("Should Serbia be a monarchy?"); 49.8% respondents expressed support in a reconstitution of monarchy, 44.6% were opposed and 5.5% were indifferent.
In 2017, an NGO, the Kingdom of Serbia Association, announced that in 2016, they had collected over 123,000 signatures of support for a referendum on Alexander being named king, short of the 150,000 needed to force a constitutional amendment.



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
  AssignClass (96363f93-f6ad-4bf9-a76f-6d68feaec230)
 Call ID: 96363f93-f6ad-4bf9-a76f-6d68feaec230
  Args:
    type: :Man
    source: Alexander_Crown_Prince_of_Yugoslavia
  AssignClass (7c86c7fd-1d68-4095-a8c2-5774eace0fc6)
 Call ID: 7c86c7fd-1d68-4095-a8c2-5774eace0fc6
  Args:
    type: :Person
    source: Alexander_Crown_Prince_of_Yugoslavia
  AssignClass (8e75017d-29f7-4c18-b69d-2e73d5f18a90)
 Call ID: 8e75017d-29f7-4c18-b69d-2e73d5f18a90
  Args:
    type: :Man
    source: King_Peter_II
  AssignClass (b80258b3-d36d-42db-b683-7d7488b6ed79)
 Call ID: b80258b3-d36d-42db-b683-7d7488b6ed79
  Args:
    type: :Person
    source: King_Peter_II
  AssignClass (dbaf046e-6f6d-4279-85e3-8ecbd3d50d01)
 Call ID: dbaf046e-6f6d-4279-85e3-8ecbd3d50d01
  Args:
    type: :Woman
    source: Queen_Alexandra_of_Yugoslavia
  AssignClass (1b2b7ed0-cea4-4793-b514-c800b3dc0550)
 Call ID: 1b2b7ed0-cea4-4793-b514-c800b3dc0550
  Args:
    type: :Person
    source: Queen_Alexandra_of_Yugoslavia
  AddTriple (893f5319-964b-4ddd-a9cd-cdc21542a353)
 Call ID: 893f5319-964b-4ddd-a9cd-cdc21542a353
  Args:
    source: Alexander_Crown_Prince_of_Yugoslavia
    relation: :hasFather
    target: King_Peter_II
  AddTriple (330acab6-f34d-459a-9353-a1c9c098becc)
 Call ID: 330acab6-f34d-459a-9353-a1c9c098becc
  Args:
    target: Queen_Alexandra_of_Yugoslavia
    relation: :hasMother
    source: Alexander_Crown_Prince_of_Yugoslavia
  AddLiteral (b4d7232f-cd31-4145-a4d6-026509d65aab)
 Call ID: b4d7232f-cd31-4145-a4d6-026509d65aab
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1945
    source: Alexander_Crown_Prince_of_Yugoslavia
  AssignClass (dc7996e8-d16e-46f3-b1de-ba92c27104ef)
 Call ID: dc7996e8-d16e-46f3-b1de-ba92c27104ef
  Args:
    type: :Woman
    source: Princess_Aspasia_of_Greece_and_Denmark
  AssignClass (9cee4d6e-baf8-47a7-af4d-9f2b31fbd972)
 Call ID: 9cee4d6e-baf8-47a7-af4d-9f2b31fbd972
  Args:
    type: :Person
    source: Princess_Aspasia_of_Greece_and_Denmark
  AssignClass (831b23a4-c0aa-4706-bde9-6c5b6c3f75b0)
 Call ID: 831b23a4-c0aa-4706-bde9-6c5b6c3f75b0
  Args:
    type: :Woman
    source: Princess_Maria_da_Gloria_of_Orleans-Braganza
  AssignClass (85510192-9ff2-4b01-a542-51c468279950)
 Call ID: 85510192-9ff2-4b01-a542-51c468279950
  Args:
    type: :Person
    source: Princess_Maria_da_Gloria_of_Orleans-Braganza
  AssignClass (a4dce1ed-b482-4f98-9668-a2ee2187dd9a)
 Call ID: a4dce1ed-b482-4f98-9668-a2ee2187dd9a
  Args:
    type: :Man
    source: Peter_son_of_Alexander
  AssignClass (e69ab561-e0d0-4892-98d2-bd1c369c1c06)
 Call ID: e69ab561-e0d0-4892-98d2-bd1c369c1c06
  Args:
    type: :Person
    source: Peter_son_of_Alexander
  AssignClass (ce2dca1a-bca7-4c33-ad8b-6bae06fab6e1)
 Call ID: ce2dca1a-bca7-4c33-ad8b-6bae06fab6e1
  Args:
    type: :Man
    source: Philip_son_of_Alexander
  AssignClass (71e6f0e4-04ae-482e-99a8-72ead408da36)
 Call ID: 71e6f0e4-04ae-482e-99a8-72ead408da36
  Args:
    type: :Person
    source: Philip_son_of_Alexander
  AssignClass (b327f0a9-d0e0-45b7-90b7-aef90e56afa5)
 Call ID: b327f0a9-d0e0-45b7-90b7-aef90e56afa5
  Args:
    type: :Man
    source: Alexander_son_of_Alexander
  AssignClass (eb83a0bb-1d6b-471f-ac84-92124d5622d2)
 Call ID: eb83a0bb-1d6b-471f-ac84-92124d5622d2
  Args:
    type: :Person
    source: Alexander_son_of_Alexander
  AddTriple (f823bfba-0bb3-497a-9cfc-68ad6b094cc7)
 Call ID: f823bfba-0bb3-497a-9cfc-68ad6b094cc7
  Args:
    relation: :hasFather
    target: Alexander_Crown_Prince_of_Yugoslavia
    source: Peter_son_of_Alexander
  AddTriple (fda372a0-37dc-4f70-a8d0-2040f136be4e)
 Call ID: fda372a0-37dc-4f70-a8d0-2040f136be4e
  Args:
    relation: :hasMother
    target: Princess_Maria_da_Gloria_of_Orleans-Braganza
    source: Peter_son_of_Alexander
  AddTriple (aa061530-581e-4085-adc2-dc2b7726bf32)
 Call ID: aa061530-581e-4085-adc2-dc2b7726bf32
  Args:
    target: Alexander_Crown_Prince_of_Yugoslavia
    relation: :hasFather
    source: Philip_son_of_Alexander
  AddTriple (9dc0dd6c-8183-4d28-81ed-c97c61efcef2)
 Call ID: 9dc0dd6c-8183-4d28-81ed-c97c61efcef2
  Args:
    source: Philip_son_of_Alexander
    relation: :hasMother
    target: Princess_Maria_da_Gloria_of_Orleans-Braganza
  AddTriple (96fb3f72-1ec0-4f4b-be19-ba3cd365b524)
 Call ID: 96fb3f72-1ec0-4f4b-be19-ba3cd365b524
  Args:
    source: Alexander_son_of_Alexander
    relation: :hasFather
    target: Alexander_Crown_Prince_of_Yugoslavia
  AddTriple (3dec8814-6031-48fd-b849-e8bfc641052c)
 Call ID: 3dec8814-6031-48fd-b849-e8bfc641052c
  Args:
    source: Alexander_son_of_Alexander
    relation: :hasMother
    target: Princess_Maria_da_Gloria_of_Orleans-Braganza
  AssignClass (8b2be677-7183-42a4-bea4-b4f61dc20c9f)
 Call ID: 8b2be677-7183-42a4-bea4-b4f61dc20c9f
  Args:
    type: :Woman
    source: Crown_Princess_Katherine
  AssignClass (07da8578-59ab-40d1-b172-f3fbedfdbfaf)
 Call ID: 07da8578-59ab-40d1-b172-f3fbedfdbfaf
  Args:
    type: :Person
    source: Crown_Princess_Katherine
  AssignClass (f8a7eff9-2a6c-435a-a185-d3633797fc9e)
 Call ID: f8a7eff9-2a6c-435a-a185-d3633797fc9e
  Args:
    type: :Man
    source: Robert_Batis
  AssignClass (e452b339-d75e-48c7-8b01-28c13214633b)
 Call ID: e452b339-d75e-48c7-8b01-28c13214633b
  Args:
    type: :Person
    source: Robert_Batis
  AssignClass (e49bd8e5-6ed7-4ee6-8d13-62e50cdfd194)
 Call ID: e49bd8e5-6ed7-4ee6-8d13-62e50cdfd194
  Args:
    type: :Woman
    source: Anna_Dosti
  AssignClass (62bc97a2-d3a5-44cc-93fa-9817dd0de123)
 Call ID: 62bc97a2-d3a5-44cc-93fa-9817dd0de123
  Args:
    type: :Person
    source: Anna_Dosti
  AddTriple (483eca66-4fb9-469f-b87b-7877f4d84d6f)
 Call ID: 483eca66-4fb9-469f-b87b-7877f4d84d6f
  Args:
    relation: :hasFather
    target: Robert_Batis
    source: Crown_Princess_Katherine
  AddTriple (0577c46c-c0ca-4296-b0c6-66f89e79564d)
 Call ID: 0577c46c-c0ca-4296-b0c6-66f89e79564d
  Args:
    target: Anna_Dosti
    relation: :hasMother
    source: Crown_Princess_Katherine
  Finish (56406d18-77ec-4c57-bf04-9712d8ecb026)
 Call ID: 56406d18-77ec-4c57-bf04-9712d8ecb026
  Args: